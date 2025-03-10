from pathlib import Path

from db.models import LessonMaterial
from utils.hash import hash_filename
from pkg.repositories import lesson_material as material_repository

from logger.logger import logger


import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def save_file(lesson_id, file):
    hashed_filename = hash_filename(file.filename)
    file.hashed_filename = hashed_filename
    material_repository.save_file(lesson_id, file)


def upload_file(lesson_id, file):
    save_file(lesson_id, file)

    lm = LessonMaterial()
    lm.lesson_id = lesson_id
    lm.filename =  file.filename
    lm.hashed_filename = file.hashed_filename
    lm.file_size_bytes = file.size    
    return material_repository.upload_file(lm)


def get_all_materials(lesson_id: int):
    logger.info("service entrypoint")
    materials = material_repository.get_all_materials(lesson_id)
    return materials


def get_material_by_id(file_id: int):
    logger.info(f"querying for file {file_id}")
    lesson_material = material_repository.get_material_by_id(file_id)
    return lesson_material


def replace_file(file_id, file):
    file_path = material_repository.get_material_by_id(file_id)
    logger.info(f"file_path: {file_path}")
    if file_path is None:
        return None
    
    hashed_filename = hash_filename(file.filename)
    file.hashed_filename = hashed_filename
    return material_repository.replace_file(Path(file_path), file)


def update_file(file_id, file):
    new_file_path = replace_file(file_id, file)
    logger.info(f"New file path: {new_file_path}")
    if new_file_path is None:    
        return None
    
    lm = LessonMaterial()
    lm.lesson_id = int(new_file_path.parent.stem)
    lm.filename = file.filename
    lm.hashed_filename = file.hashed_filename
    lm.file_size_bytes = file.size
    return material_repository.update_file(file_id, lm)