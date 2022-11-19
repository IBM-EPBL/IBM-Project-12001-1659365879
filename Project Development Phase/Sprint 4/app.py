from flask import Flask, render_template, request
from math import ceil
import pickle
import requests

app = Flask(__name__)
# model = pickle.load(open("model1.pkl","rb"))

# fetching the ML model from the IBM Deployment space

API_KEY = "TpADwrsyFnYatIlV70EKAo9NQtUrr7HaZsR7TUREFkMR"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
    "apikey":API_KEY, 
    "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
})
mltoken = token_response.json()["access_token"]
header = {
    'Content-Type': 'application/json', 
    'Authorization': 'Bearer ' + mltoken
}


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
    
    payload_scoring = {"input_data": [{
        "fields": [["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]], 
        "values": [[gre,toefl,rating,sop,lor,cgpa,research]]
    }]}
    
    # fetching the prediction result..
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b47f221e-15b5-4c30-a265-8174210f27b3/predictions?version=2022-11-19', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    # print("Scoring response")
    # print(response_scoring.json())
    
    temp = response_scoring.json()
    result = temp["predictions"][0]['values'][0][0]
    
    if result > 0.5:
        return render_template("chance.html",msg="Congratulation, you are eligible. As the probability is " + str(ceil(result*100))+"%")
    return render_template("nochance.html",msg="Sorry, Unfortunately you aren't eligible. As the probability is " + str(ceil(result*100))+"%")

if __name__ == "__main__":
    app.run(debug=True)