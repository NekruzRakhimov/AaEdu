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


def get_material_by_hashed_filename(hashed_filename: str):
    logger.info(f"uqerying for file {hashed_filename}")
    lesson_material = material_repository.get_material_by_hashed_filename(hashed_filename)
    return lesson_material