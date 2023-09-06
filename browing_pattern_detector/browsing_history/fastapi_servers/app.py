import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import URLDetails
from MLModel.model import *
app = FastAPI() 
import requests 
import json 

origins = [
    "*"
]

ACCESS_TOKEN_FILE_NAME = "/home/mukesh/access_token/accesstoken.json"
UPDATE_BROWSING_ENDPOINT = "http://127.0.0.1:8080/browsing_history/add_user_browsing_history"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
json_obj = json.load(open(ACCESS_TOKEN_FILE_NAME))
@app.post("/send_url")
async def send_url(data : URLDetails):
    global json_obj
    print(json_obj)
    access_token = json_obj['access_token']
    print(access_token)
    data = data.dict()
    if data['url'] != '' and data['url'].startswith('chrome://') == False : 
        domain = re.search(r"([^/]*/){2}([^/]*)", data['url']).group(0)
        category=prediction(domain)
        res = requests.post(UPDATE_BROWSING_ENDPOINT, json = {
            'access_token': access_token,
            'url': domain,
            'type_of_website': category
        })
    return {
    'status': "Success"
    }

@app.post("/quit_url")
async def quit_url(data : URLDetails): 
    print(data)
    data = data.dict()
    return {
        'status': "Success"
    }
