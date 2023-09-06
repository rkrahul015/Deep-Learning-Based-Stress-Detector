from fastapi import APIRouter
from .validator import *
from db.database import *

'''
/register/student_register
/register/employee_register
'''

student_registration_router = APIRouter(
    prefix="/register",
    tags=["register"]
)

@student_registration_router.post("/student_register")
async def registerStudent(student_data: StudentModel):
    student_data = student_data.dict()
    print(student_data)
    if(UserRegistration(
        username=student_data['user_name'],
        first_name=student_data['first_name'],
        last_name=student_data['last_name'],
        email=student_data['email'],
        password=student_data['pass_word'],
        phone=student_data['contact'],
        interval=student_data['reportingTime'],
        placeholder='student'
    )):
        return {
            # "result": student_data,
            'status_code': 200,
            'message': 'success',
            'data': []
        }
    else:
        return {
            # "result": "Not saved"
            'status_code': 400,
            'message': "User Not Created",
            'data': []
        }

employee_registration_router = APIRouter(
    prefix="/register",
    tags=["register"]
)

@employee_registration_router.post("/employee_register")
async def register_employee(employee_data: EmployeeModel):
    employee_data = employee_data.dict()
    print(employee_data)
    if(UserRegistration(
        username=employee_data['user_name'],
        first_name=employee_data['first_name'],
        last_name=employee_data['last_name'],
        email=employee_data['email'],
        password=employee_data['pass_word'],
        phone=employee_data['contact'],
        interval=employee_data['reportingTime'],
        placeholder='employee'
    )):
        return {
            # "result": employee_data,
            "status_code": 200,
            "message": "Success",
            "data": {}
        }
    else:
        return {
            "status_code": 200,
            "message": "Success",
            "data": {}
        }