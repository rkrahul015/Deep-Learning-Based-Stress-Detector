from pydantic import BaseModel 

class BrowingDetails(BaseModel):
    access_token    : str
    url             : str 
    type_of_website : str

class UserBrowsingDetails(BaseModel): 
    access_token    : str 