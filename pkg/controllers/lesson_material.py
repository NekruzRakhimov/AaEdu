import json

from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile
from starlette.responses import Response, JSONResponse

from pkg.controllers.middlewares import get_current_user
from logger.logger import logger
from utils.auth import TokenPayload

from pathlib import Path
import shutil

from pkg.services import lesson_material as material_service


import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


BYTES_TO_MB = 1048576
MAX_ALLOWED_SIZE = 1048576 * 5


router = APIRouter()


# CREATE
@router.post("/lesson-material/{lesson_id}", summary="Upload a file", tags=["lesson-material"])
def upload_file(lesson_id: str, file: UploadFile = File(...)):
    
    if file.size > MAX_ALLOWED_SIZE:
        return {"error": "File size should be less or equal to 5mb"}
    
    try:
        material_service.upload_file(lesson_id, file)
        return {
            "message": "file uploaded successfully",
        }
    except Exception as e:
        return {"message": e.args}


# @router.get("/content", summary="Get all content", tags=["content"])
# def get_all_content():  #payload: TokenPayload=Depends(get_current_user)):
#     return JSONResponse({"message": str(CONTENT_STORAGE)}, status_code=status.HTTP_200_OK)