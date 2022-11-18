from flask import Flask, render_template, request
from math import ceil
import pickle

app = Flask(__name__)
model = pickle.load(open("model1.pkl","rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=["GET","POST"])
def predict():
    gre=(eval(request.form["gre"])-290)/(340-290)
    toefl=(eval(request.form["toefl"])-92)/(120-92)
    rating=(eval(request.form["rating"])-1.0)/4.0
    sop=(eval(request.form["sop"])-1.0)/4.0
    lor=(eval(request.form["lor"])-1.0)/4.0
    cgpa=(eval(request.form["cgpa"])-6.7)/(10.0-6.7)
    research=request.form["research"]
    if research == 1:
        research = 1
    else:
        research = 0
    pred = [[gre,toefl,rating,sop,lor,cgpa,research]]
    result=model.predict(pred)
    if result > 0.5:
        return render_template("chance.html",msg="Congratulation, you are eligible. As the probability is "+str(ceil(result[0]*100))+"%")
    return render_template("nochance.html",msg="Sorry, Unfortunately you aren't eligible. As the probability is "+str(ceil(result[0]*100))+"%")

if __name__ == "__main__":
    app.run(port=8801)