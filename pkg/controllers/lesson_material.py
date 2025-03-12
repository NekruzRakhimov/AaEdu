import json

from fastapi import APIRouter, status, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.responses import Response, JSONResponse
from pathlib import Path

from pkg.controllers.middlewares import get_current_user
from utils.auth import TokenPayload
from pkg.services import lesson_material as material_service
from logger.logger import logger


BYTES_TO_MB = 1048576
MAX_ALLOWED_SIZE = 1048576 * 5


router = APIRouter()


@router.get("/")
def ping_pong():
    return {"ping": "pong"}


# CREATE
@router.post("/lesson-materials/{lesson_id}", summary="Upload a file", tags=["lesson_materials"])
def upload_file(lesson_id: int, file: UploadFile = File(...), payload: TokenPayload=Depends(get_current_user)):
    role_id = payload.role_id
    logger.info(f"role_id: {role_id}")
    if role_id == 1:
        return JSONResponse({"error": "only admins and mentors can add lesson materials"},
                        status_code=status.HTTP_403_FORBIDDEN)
    
    logger.info(f"file size: {file.size}")
    if file.size > MAX_ALLOWED_SIZE:
        return JSONResponse({"error": "File size should be less or equal to 5mb"})

    if not material_service.get_material_by_filename(file.filename) is None:    
        return JSONResponse({"error": f"File {file.filename} already exists"})

    try:
        material_service.upload_file(lesson_id, file)
        return JSONResponse({
            "message": "file uploaded successfully",
        }, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse({"message": e.args})


# READ
@router.get("/lesson-materials/{lesson_id}", summary="Get list of all lesson_materials", tags=["lesson_materials"])
def get_all_materials(lesson_id: int, payload: TokenPayload=Depends(get_current_user)):
    try:
        materials = material_service.get_all_materials(lesson_id)
        return materials
    except Exception as e:
        return JSONResponse({"message": e.args})


@router.get("/lesson-materials/file/{file_id}", summary="Get lesson material by id", tags=["lesson_materials"])
def get_material_by_id(file_id: int, payload: TokenPayload=Depends(get_current_user)):
    try:
        file_to_download = material_service.get_material_by_id(file_id)
        logger.info(f"controller layer->get_material_by_id->file_to_download = {file_to_download}")
        if file_to_download is None:
            return JSONResponse(
                {"error": "The requested file not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        file_path, filename = file_to_download
        logger.info(f"controller layer->get_material_by_id->file_exists={Path(file_path).exists()}")
        if not Path(file_path).exists():
            return JSONResponse(
                {"error": "The requested file does not exist on the server"},
                status_code=status.HTTP_410_GONE
            )
        return FileResponse(file_path, filename=filename)
    except Exception as e:
        return {"message": e.args}
    

# UPDATE
@router.put("/lesson-materials/file/{file_id}", summary="Update lesson material by id", tags=["lesson_materials"])
def update_file(file_id: int, file: UploadFile = File(...), payload: TokenPayload = Depends(get_current_user)):
    role_id = payload.role_id
    if role_id == 1:
        return Response(json.dumps({"error": "only admins and mentors can update lesson materials"}),
                        status_code=status.HTTP_403_FORBIDDEN)
    
    if file.size > MAX_ALLOWED_SIZE:
        return JSONResponse({"error": "File size should be less or equal to 5mb"})
    
    try:
        new_file_path = material_service.update_file(file_id, file)
        if new_file_path is None:
            return JSONResponse(
                {"error": "The requested file not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        if new_file_path:
            return JSONResponse({
                "message": "file updated successfully",
            }, status_code=status.HTTP_200_OK)
    except Exception as e:
        return {"message": e.args}
    

# DELETE
@router.delete("/lesson-materials/file/{file_id}", summary="Delete lesson material by id", tags=["lesson_materials"])
def delete_file(file_id, payload: TokenPayload = Depends(get_current_user)):
    role_id = payload.role_id
    if role_id == 1:
        return JSONResponse({"error": "only admins and mentors can delete lesson materials"},
                        status_code=status.HTTP_403_FORBIDDEN)
    
    if material_service.delete_file(file_id):
        return JSONResponse({
            "message": "successfully deleted the file"
        }, status_code=status.HTTP_200_OK)