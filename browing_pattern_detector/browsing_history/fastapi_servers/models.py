from pydantic import BaseModel 

class URLDetails(BaseModel): 
    url: str 
    access_key: str