import dotenv
import os

from pydantic import BaseModel, Field

from app.schemas.chatImage_models import ChatImageUpload
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

from fastapi import APIRouter, Body, File, Form, Path, Query, UploadFile
from typing import List
from PIL import Image
from io import BytesIO
from ..services.image_service import imageService

router = APIRouter()

@router.post(path='/uploadImagesToS3/{spotType}', description='chat image를 제외한 모든 이미지를 핸들링합니다.',)
async def uploadImage(
    spotType: str = Path(...,description="please check image type. in case of bigspot / spot / userprofile "),
    files: List[UploadFile] = File(..., description="please upload image file")
    ):
    
    imageObj = await imageService.normalImage_upload(spotType.lower(),files)

    return {"file":imageObj}

# 메시지 아이디와 이미지를 받아서 레디스에 데이터 업데이트.
# 채팅에서 올라온 이미지 리액션 핸들링을 위한 우선처리.
@router.post("/uploadChatImage", description="유저 chat 이미지를 s3에 저장하고 디비에 기록합니다.")
# async def upload(chatModel: ChatImageUpload = Body(..., description="유저 아이디와 메시지 아이디를 포함한 요청 바디")):
async def upload(
    files: List[UploadFile] = File(..., description="List of image files"),
    type: str = Form(..., description="personal // bigspot // spot"),
    pk: int = Form(..., description="spot pk")
    ):
    # print(chatModel.pk)
    imageName = await imageService.chatImage_upload(files,type,pk)

    return {"file": imageName}

@router.post("/test", description="docker test.")
# async def upload(chatModel: ChatImageUpload = Body(..., description="유저 아이디와 메시지 아이디를 포함한 요청 바디")):
async def test():
    return {"success"} 