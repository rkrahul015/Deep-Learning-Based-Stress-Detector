from pydantic import BaseModel 
from typing import List 

class StressBlinkValue(BaseModel):
    stress_list_lst : List[int]
    timestamp : str
    blink_count : int
    access_token : str


class GetStressBlinkData(BaseModel):
    access_token: str 