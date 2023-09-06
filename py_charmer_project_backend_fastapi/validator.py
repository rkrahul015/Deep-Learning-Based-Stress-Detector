from pydantic import BaseModel
from typing import Optional


class StudentModel(BaseModel):
    user_name: str
    first_name: str
    last_name: Optional[str]
    email: str
    pass_word: str
    contact: str
    acc_token: str


class EmployeeModel(BaseModel):
    user_name: str
    first_name: str
    last_name: Optional[str]
    email: str
    pass_word: str
    contact: str
    acc_token: str


class StressDataModel(BaseModel):
    time: str
    stressLevel: float


class ScreenTimeDataModel(BaseModel):
    time: str
    screenTimeSpeed: int


class TypingDataModel(BaseModel):
    time: str
    typingSpeed: int
