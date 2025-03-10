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
@router.post("/lesson-materials/{lesson_id}", summary="Upload a file", tags=["lesson-materials"])
def upload_file(lesson_id: int, file: UploadFile = File(...)):
    
    if file.size > MAX_ALLOWED_SIZE:
        return {"error": "File size should be less or equal to 5mb"}
    
    try:
        material_service.upload_file(lesson_id, file)
        return JSONResponse({
            "message": "file uploaded successfully",
        }, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return {"message": e.args}


# READ
@router.get("/lesson-materials/{lesson_id}", summary="Get list of all lesson_materials", tags=["lesson_materials"])
def get_all_materials(lesson_id: int):  #payload: TokenPayload=Depends(get_current_user)):
    try:
        materials = material_service.get_all_materials(lesson_id)
        return materials
    except Exception as e:
        return {"message": e.args}


@router.get("/lesson-materials/file/{file_id}", summary="Get lesson material by id", tags=["lesson_materials"])
def get_material_by_id(file_id: int):
    try:
        lesson_material = material_service.get_material_by_id(file_id) 
        return JSONResponse({"lesson_material path": lesson_material}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return {"message": e.args}
    
# UPDATE
@router.put("/lesson-materials/file/{file_id}", summary="Update lesson material by id", tags=["lesson_materials"])
def update_file(file_id: int, file: UploadFile = File(...)):
    if file.size > MAX_ALLOWED_SIZE:
        return {"error": "File size should be less or equal to 5mb"}
    
    try:
        new_file_path = material_service.update_file(file_id, file)
        if new_file_path:
            return JSONResponse({
                "message": "file updated successfully",
            }, status_code=status.HTTP_200_OK)
    except Exception as e:
        return {"message": e.args}