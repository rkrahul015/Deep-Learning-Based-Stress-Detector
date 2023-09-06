# python main.py

from fastapi import FastAPI
import uvicorn
from validator import *
from db.database import *
from user_registration.index import student_registration_router, employee_registration_router
from login.index import user_router
from url_handling.index import new_extension_router, delete_extension_router
from stress_blink_data.index import stress_blink_router
from browsinghistory.index import browser_api_router
from alert_system.index import alert_router

app = FastAPI()
app.include_router(student_registration_router)
app.include_router(employee_registration_router)
app.include_router(user_router)
app.include_router(new_extension_router)
app.include_router(delete_extension_router)
app.include_router(stress_blink_router)
app.include_router(browser_api_router)
app.include_router(alert_router)