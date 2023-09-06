from fastapi import APIRouter
from .validator import *
from db.database import *

new_extension_router = APIRouter(
    prefix="/url",
    tags=["url"]
)
@new_extension_router.post("/new")
async def newExtensionRouter(extension_data: NewExtensionModel):
    extension_data=extension_data.dict()
    print(extension_data)
    try:
        CreateUrl(
            username = extension_data['username'],
            url = extension_data['url'],
        )
        return {
            "result": "url stored successfully",
        }
    except:
        return {
            "result": "url has not stored successfully",
        }

delete_extension_router = APIRouter(
    prefix="/url",
    tags=["url"]
)
@new_extension_router.post("/delete")
async def deleteExtensionRouter(extension_data: NewExtensionModel):
    extension_data=extension_data.dict()
    print(extension_data)
    try:
        DeleteUrl(
            username = extension_data['username'],
            url = extension_data['url'],
        )
        return {
            "result": "url deleted successfully",
        }
    except:
        return {
            "result": "url has not deleted successfully",
        }