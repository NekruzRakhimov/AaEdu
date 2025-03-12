from sqlalchemy.orm import Session
from pathlib import Path
import shutil

import datetime

from db.postgres import engine
from db.models import LessonMaterial
from logger.logger import logger


import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


MATERIAL_STORAGE = Path(Path.cwd(), 'lesson_materials')


def save_file(lesson_id, file):
    try:
        subfolder = Path(MATERIAL_STORAGE, str(lesson_id))
        if not subfolder.exists():
            subfolder.mkdir(parents=True)
        file_path = Path(subfolder, file.hashed_filename)
        
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        
    except Exception as e:
        return {"message": e.args}


def upload_file(lesson_material: LessonMaterial):
    try:    
        with Session(bind=engine) as db:
            db.add(lesson_material)
            db.commit()
            return lesson_material.id
    except Exception as e:
        return {"message": e.args}


def get_all_materials(lesson_id):
    try:
        with Session(bind=engine) as db:
            db_materials = db.query(LessonMaterial).filter(
                LessonMaterial.deleted_at == None,
                LessonMaterial.lesson_id == lesson_id
            ).all()

            return db_materials
    except Exception as e:
        return {"message": e.args}
    

def get_material_by_filename(filename):
    with Session(bind=engine) as db:
        db_material = db.query(LessonMaterial).filter(
            LessonMaterial.deleted_at == None,
            LessonMaterial.filename == filename
        ).first()
        logger.info(f"query returned: {db_material}")
        if db_material is None:
            logger.error(f"Filename {filename} not found")
            return None
        return db_material
    

def get_material_by_id(file_id):
    with Session(bind=engine) as db:
        db_material = db.query(LessonMaterial).filter(
            LessonMaterial.deleted_at == None,
            LessonMaterial.id == file_id
        ).first()
        logger.info(f"query returned: {db_material}")
        if db_material is None:
            logger.error(f"File ID {file_id} not found")
            return None
        
        file_path = str(Path(MATERIAL_STORAGE, str(db_material.lesson_id), db_material.hashed_filename))
        logger.info(f"rep layer->get_material_by_id->file_path={file_path}, filename={db_material.filename}")
        # if not file_path.exists():
        #     return None
        return (file_path, db_material.filename)
    

def replace_file(file_path, file):
    try:
        file_path = Path(file_path)
        logger.info(f"repo layer->replace_file->file_path is Path={isinstance(file_path, Path)}")
        if not file_path.exists():
            return None
        
        file_path.unlink()  # удаляем старый файл
        new_file_path = Path(file_path.parent, file.hashed_filename)
        logger.info(f"repo layer->replace_file->new_file_path={new_file_path}")
        with open(new_file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        return new_file_path
    
    except Exception as e:
        return {"message": e.args}
    

def update_file(file_id, lesson_material):
    with Session(bind=engine) as db:
        db_material = db.query(LessonMaterial).filter(
                LessonMaterial.deleted_at == None,
                LessonMaterial.id == file_id
            ).first()
        
        if db_material is None:
            return None
        
        db_material.filename = lesson_material.filename
        db_material.hashed_filename = lesson_material.hashed_filename
        db_material.file_size_bytes = lesson_material.file_size_bytes
        db_material.updated_at = datetime.datetime.now()
        db.commit()

        return db_material.id
    

def delete_file(file_id):
    with Session(bind=engine) as db:
        db_material = db.query(LessonMaterial).filter(
                LessonMaterial.deleted_at == None,
                LessonMaterial.id == file_id
            ).first()
        
        if db_material is None:
            return None
        
        db_material.deleted_at = datetime.datetime.now()
        db.commit()
        return db_material.id