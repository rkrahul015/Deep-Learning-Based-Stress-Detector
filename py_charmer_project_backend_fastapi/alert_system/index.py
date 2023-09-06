from fastapi import APIRouter 
from .validators import UserDetails
from stress_blink_data.index import get_stress_blink_data
from browsinghistory.index import get_user_browsing_details
import numpy as np

alert_router = APIRouter(
    prefix = "/alert",
    tags = ["alert"]
)


@alert_router.post("/get_alert")
async def send_alert(user_details : UserDetails):
    user_details = user_details.dict()
    ### fetch stress rate 
    stress_blink_data = await get_stress_blink_data({ 'access_token' : user_details['access_token'] })
    data = stress_blink_data['data']
    stress_level_lst = data['stress_level_lst'] if len(data['stress_level_lst']) < 10 else data['stress_level_lst'][-10:]
    eye_blink_lst = data['blink_count_lst'] if len(data['blink_count_lst']) < 10 else data['blink_count_lst'][-10:]
    
    dict_value = {}
    max_val = stress_level_lst[0]
    for s in stress_level_lst: 
        if s not in dict_value: 
            dict_value[s] = 1 
        else: 
            dict_value[s] += 1 
        if dict_value[s] > dict_value[max_val]:
            max_val = s 
        
    alert_pointers = []   
    print(stress_level_lst)
    print(eye_blink_lst)
    if max_val > 75: 
        alert_pointers.append("Your Stress Level since Last Few Minutes Shows High.")

    if np.std(eye_blink_lst) > 3: 
        alert_pointers.append("Your Eye Blinking Rate Changed Drastically Over Last Few Minutes.")

    browsing_details = await get_user_browsing_details({'access_token' : user_details['access_token']})
    browsing_details = browsing_details['data'][-1]
    type_of_browsing_details = browsing_details['type']
    print(type_of_browsing_details)
    if  'Adult' in type_of_browsing_details.keys() and type_of_browsing_details['Adult'] > 20: 
        alert_pointers.append("You should take care about content you see on internt.")
    
    elif 'Shopping' in type_of_browsing_details.keys() and type_of_browsing_details['Shopping'] > 20:
        alert_pointers.append("You should avoid Shooping Website, you are getting obsessed with it.")
    if len(alert_pointers) == 0:
        alert_pointers.append("Everything Looks nice, Have a Good Day.")
    return {
        'status': 200,
        'message': 'SuccessFull',
        'data': {
            'alert': alert_pointers
        }
    }
