from typing import List
from fastapi import File, UploadFile
from pydantic import BaseModel

class ChatImageUpload(BaseModel):
    type: str
    pk: int
    
    
