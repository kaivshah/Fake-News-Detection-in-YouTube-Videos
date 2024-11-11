from flask import Flask, escape, request, render_template
import pickle 
from youtube_transcript_api import YouTubeTranscriptApi
from sklearn.feature_extraction.text import CountVectorizer
import sklearn.feature_extraction.text


vector = pickle.load(open("vectorizer.pkl",'rb'))
model=pickle.load(open("finalized_model.pkl",'rb'))
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/prediction",methods=['GET','POST'])
def prediction():
    if request.method =="POST":
        news = str(request.form['news'])
        outls = []
        tx = YouTubeTranscriptApi.get_transcript(news,languages=['en'])
        for i in tx:
            outtxt = (i['text'])
            outls.append(outtxt)

        with open("op.txt","a") as opf:
            opf.write(outtxt + "\n")

        vectorizer = CountVectorizer()
        vectorizer.fit(outls)
        
        print("Vocubulary ",vectorizer.vocabulary_ )
        #print(news)
        print(outls)

        str1 = "" 
    
        # traverse in the string  
        for ele in outls:
            if ele == " ":
                str1 += " "
            else:
             str1 += ele + " " 
        
        print("str1", str1)
     
        predict = model.predict(vector.transform([str1]))
        print(predict)
        

        if predict== 0 :
           return render_template("prediction.html",link=news,prediction_text="The information present in this video is REAL.".format(predict))
        elif predict== 1 :
           return render_template("prediction.html",link=news, prediction_text="The information present in this video is FALSE.".format(predict))
        else:
            return render_template("prediction.html",link=news, prediction_text="The information present in this video is DEBUNKING.".format(predict))      
         #  return render_template("prediction.html", prediction_text="News Content is -> DEBUNKING i.e {}".format(predict))      
        #return render_template("prediction.html", prediction_text="News Headline is -> {}".format(predict))



    else:
        return render_template("prediction.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ =='__main__':
    app.run()
