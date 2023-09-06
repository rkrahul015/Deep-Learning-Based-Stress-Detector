from fastapi import APIRouter 
from .validators import BrowingDetails, UserBrowsingDetails
from setup import pycharmer_mongo_db
from datetime import datetime 

browser_api_router = APIRouter(
    prefix="/browsing_history",
    tags = ["browsing_history"]
)

@browser_api_router.post("/add_user_browsing_history")
async def add_user_browing_hist(browsing_details : BrowingDetails):
    browsing_details = browsing_details.dict()
    str_date = str(datetime.now().date())
    print(str_date)
    res = pycharmer_mongo_db.browser_pattern.find({"access_token" : browsing_details['access_token'],
        'date': str_date
        }) 
    count = 0
    for i in res:
        count += 1
    if count == 0:
        pycharmer_mongo_db.browser_pattern.insert({
            "access_token": browsing_details['access_token'],
            "date": str_date,
            "url_lst": [browsing_details['url']],
            "type_of_website": [browsing_details['type_of_website']]
        })
    else:
        pycharmer_mongo_db.browser_pattern.update( {'access_token': browsing_details['access_token'], 'date' : str_date},
            {
                "$push": {
                    "url_lst": browsing_details['url'],
                    'type_of_website': browsing_details['type_of_website']
                }
            }
        )
    return {
        "message": "success"
    }

    
@browser_api_router.post("/get_user_browsing_details")
async def get_user_browsing_details(user_browsing_details : UserBrowsingDetails): 
    if type(user_browsing_details) != dict:
        user_browsing_details = user_browsing_details.dict()
    access_token = user_browsing_details['access_token']
    browsing_data = []
    res = pycharmer_mongo_db.browser_pattern.find({"access_token": access_token})
    for obj in res: 
        details = {}
        details['date'] = obj['date']
        details['url_visit_count'] = {}
        details['type'] = {}
        for url in obj['url_lst']: 
            if url not in details['url_visit_count']: 
                details['url_visit_count'][url] = obj['url_lst'].count(url)
        
        for t in obj['type_of_website']: 
            if t not in details['type']:
                details['type'][t] = obj['type_of_website'].count(t)
        browsing_data.append(details)
    return {
        "message" : "success",
        "data"    : browsing_data,
        "status"  : 200
    }