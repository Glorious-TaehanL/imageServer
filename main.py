from fastapi import FastAPI
from app.controllers.image_controller import router

app = FastAPI(
    title="ImageAPI",
    description="This server is compress image and upload s3",
    version='1.0.1'
)

app.include_router(router)
