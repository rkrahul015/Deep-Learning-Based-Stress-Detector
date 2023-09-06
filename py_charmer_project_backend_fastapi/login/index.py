from fastapi import APIRouter
from .validator import *
from db.database import *

'''
/user/login
'''

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.post("/login")
async def userLogin(login_data: LoginModel):
    login_data = login_data.dict()
    print(login_data)
    user_details = UserLogin(
        email=login_data['email'], 
        pwd=login_data['pass_word'],
        placeholder="student"
    )
    if len(user_details) == 0:
        return {
            'status_code': 400,
            'message': "Invalid Credentials",
            'data': {}
        } 
    else: 
        return {
            'status_code': 200,
            'message': "Success",
            'data': {
                'access_token': user_details[0][0]
            }
        }