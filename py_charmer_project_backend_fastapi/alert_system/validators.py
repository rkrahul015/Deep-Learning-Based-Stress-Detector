from pydantic import BaseModel 

class UserDetails(BaseModel): 
    access_token: str 