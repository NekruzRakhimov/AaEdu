from utils.hash import hash_filename
from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile

from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from db.postgres import engine
from db.models import LessonMaterial

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MATERIAL_STORAGE = Path(Path.cwd(), 'lesson_materials')


def save_file(lesson_id, file):
    try:
        subfolder = Path(MATERIAL_STORAGE, lesson_id)
        if not subfolder.exists():
            subfolder.mkdir(parents=True)
        file_path = Path(subfolder, file.hashed_filename)
        
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        
    except Exception as e:
        return {"message": e.args}


def upload_file(lesson_material: LessonMaterial):
    
    with Session(bind=engine) as db:
        db.add(lesson_material)
        db.commit()
        return lesson_material.id

    