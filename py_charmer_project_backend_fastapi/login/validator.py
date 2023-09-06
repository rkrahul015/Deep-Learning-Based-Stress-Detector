from pydantic import BaseModel

class LoginModel(BaseModel):
    email: str
    pass_word: str