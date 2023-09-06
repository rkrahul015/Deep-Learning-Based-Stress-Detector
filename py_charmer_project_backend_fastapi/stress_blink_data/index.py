from fastapi import APIRouter 
from setup import mongo_client
stress_blink_router = APIRouter(
    prefix="/stress_blink_value",
    tags = ["stress_blink_value"]
)
from .validator import StressBlinkValue, GetStressBlinkData
from setup import pycharmer_mongo_db

@stress_blink_router.post("/add_stress_blink_values") 
async def add_stress_blink_values(stressBlinkValue : StressBlinkValue):
    stress_blink_value = stressBlinkValue.dict()
    pycharmer_mongo_db.stress_blink_data.insert(stress_blink_value)
    return {
        "status_code" : 200,
        "message": "Success",
        "data": {}
    }

@stress_blink_router.post("/get_stress_blink_values") 
async def get_stress_blink_data(getStressBlinkValues : GetStressBlinkData):
    if type(getStressBlinkValues) != dict:
        get_stress_blink_data = getStressBlinkValues.dict() 
    else: 
        get_stress_blink_data = getStressBlinkValues
    data = pycharmer_mongo_db.stress_blink_data.find({"access_token": get_stress_blink_data['access_token']}) 
    time_stamp_lst = []
    blink_count = []
    stress_level = []
    for i in data:
        time_stamp_lst.append(i['timestamp'])
        blink_count.append(i['blink_count'])
        stress_level.append(max(i['stress_list_lst']))
    return {
        "status_code" : 200,
        "message": "Success",
        "data": {
            'time_stamp_lst' : time_stamp_lst,
            'blink_count_lst' : blink_count,
            'stress_level_lst' : stress_level
        }
    }
    
