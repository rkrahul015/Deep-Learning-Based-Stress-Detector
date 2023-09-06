from pydantic import BaseModel
from typing import Optional


class StudentModel(BaseModel):
    user_name: str
    first_name: str
    last_name: Optional[str]
    email: str
    pass_word: str
    contact: str
    reportingTime: str


class EmployeeModel(BaseModel):
    user_name: str
    first_name: str
    last_name: Optional[str]
    email: str
    pass_word: str
    contact: str
    reportingTime: str