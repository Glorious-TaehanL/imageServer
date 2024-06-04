import uuid
import os
import logging

from datetime import datetime
from fastapi import File, Form, HTTPException, UploadFile
from typing import List
from PIL import Image
from io import BytesIO

from app.schemas.chatImage_models import ChatImageUpload
from app.utils.mysql_utils import mysql_connection
from app.utils.s3_utils import s3_connection


async def compress_and_save_image(image_buffer: BytesIO, location: str):
    origin_image = Image.open(image_buffer)
    thumb_image = origin_image.copy()

    # 이미지의 가로와 세로 크기를 가져옵니다.
    width, height = origin_image.size

    # 이미지의 가로 또는 세로 중 더 긴 쪽을 기준으로 비율을 계산합니다.
    if width >= height:
        new_width = 1400
        new_height = int(height * (new_width / width))
    else:
        new_height = 1400
        new_width = int(width * (new_height / height))

    # 이미지를 새로운 크기로 조정합니다.
    origin_image = origin_image.resize((new_width, new_height))
    thumb_image.thumbnail((new_width, new_height))

    # image compress and modify quality
    quality_level = 85
    image_thumb_buffer = BytesIO()
    image_origin_buffer = BytesIO()
    thumb_image.save(image_thumb_buffer, format="WEBP", quality=quality_level)
    origin_image.save(image_origin_buffer, format="WEBP")

    # BytesIO file pointer move.
    image_thumb_buffer.seek(0)
    image_origin_buffer.seek(0)

    # save image on s3
    image_name = datetime.now().strftime('%m%d%H%M') + str(uuid.uuid4()) + ".webp"
    logging.error(f"${image_name} created")
    image_thumb_name = location + "thumb_" + image_name
    image_origin_name = location + "origin_" + image_name

    s3 = s3_connection()
    s3.upload_fileobj(image_thumb_buffer, os.environ['AWS_S3_BUCKET_NAME'], image_thumb_name)
    s3.upload_fileobj(image_origin_buffer, os.environ['AWS_S3_BUCKET_NAME'], image_origin_name)

    return {
        "thumbnail": image_thumb_name,
        "origin": image_origin_name
    }


def setup_logging():
    logging.basicConfig(filename='log/error/error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class imageService:
    @staticmethod
    async def normalImage_upload(type: str, files: List[UploadFile] = File(...)):
        setup_logging()
        fileName = []

        for file in files:
            try:
                max_file_size = 20 * 1024 * 1024  # 20MB
                if file.size > max_file_size:
                    raise HTTPException(status_code=413, detail="File size exceeds the limit")

                imageFile = await file.read()

                if type in ["spot", "bigspot", "userprofile"]:
                    location = "images/" + type + "/"
                else:
                    raise HTTPException(status_code=400, detail="Invalid image type params")

                result = await compress_and_save_image(BytesIO(imageFile), location)
                fileName.append(result)

                await file.close()  # 파일을 닫아 메모리를 해제합니다.

            except Exception as e:
                logging.error(f"An error occurred while call type[{type}]: {e}")

        return fileName

    @staticmethod
    async def chatImage_upload(
        files: List[UploadFile] = File(...),
        type: str = Form(...),
        pk: int = Form(...)
        ):

        setup_logging()
        fileName = []

        for file in files:
            try:
                imageFile = await file.read()

                max_file_size = 20 * 1024 * 1024  # 20MB
                if file.size > max_file_size:
                    raise HTTPException(status_code=413, detail="File size exceeds the limit")

                if type == "personal":
                    location = f"images/chat/{type}/"
                else:
                    location = f"images/chat/{type}/{pk}/"

                result = await compress_and_save_image(BytesIO(imageFile), location)
                fileName.append(result)

                await file.close()  # 파일을 닫아 메모리를 해제합니다.

            except Exception as e:
                logging.error(f"An error occurred while uploading chat image: {e}")

        return fileName
