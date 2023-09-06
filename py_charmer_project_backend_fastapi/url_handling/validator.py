from pydantic import BaseModel

class NewExtensionModel(BaseModel):
    username: str
    url: str