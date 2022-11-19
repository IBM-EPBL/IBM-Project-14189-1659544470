
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle as p

import requests 

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "0-i2jKeCb2tt5a0LKr4GDO1G5KH69tskpiHntRemiz14"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)
model=p.load(open('Kidney_Disease.pk1','rb'))
@app.route('/')
def HOME():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')   

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "JhrY6sRjbDvE3BjbiXEiTHfBCleWtA4aHZQ_7iIDL0qe"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field":[['age','blood_urea','blood glucose random','coronary_artery_disease',
                   'anemia','pus_cell','red_blood_cell','diabetesmellitus','pedal_edema']]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5fe68712-4338-4ea2-a6c3-13c0c4e0c562/predictions?version=2022-11-19', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print(response_scoring.json())
@app.route('/predict',methods=['POST'])
def prediction():    
    form_value=request.form.values()    
    data=[]
    for x in form_value:
        data.append(pd.to_numeric(x).astype(float))
    features_value=[np.array(data)]  
    features_name=['age','blood_urea','blood glucose random','coronary_artery_disease',
                   'anemia','pus_cell','red_blood_cell','diabetesmellitus','pedal_edema']
    df=pd.DataFrame(features_value, columns=features_name)
    
    output=model.predict(df)
    if(output==0):
        return render_template('index.html' , pred='Oops!! You have Kidney Chronic Disease. So, please concern a Doctor')
    else:
        return render_template('index.html' , pred='you are not affected by Chronic kidney Disease')

if __name__=='__main__':
    app.run(debug=True)


