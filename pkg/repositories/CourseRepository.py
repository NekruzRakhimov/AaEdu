from sqlalchemy.orm import Session
from db.models import Course
from pkg.schemas.CourseSchemas import CourseCreate, CourseUpdate
from datetime import datetime

class CourseRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Course).filter(Course.deleted_at == None).all()

    @staticmethod
    def get_by_id(db: Session, course_id: int):
        return db.query(Course).filter(Course.id == course_id, Course.deleted_at == None).first()

    @staticmethod
    def create(db: Session, course_data: CourseCreate):
        new_course = Course(name=course_data.name)
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course

    @staticmethod
    def update(db: Session, course, course_data: CourseUpdate):
        if course_data.name:
            course.name = course_data.name
        course.updated_at = datetime.now()
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete(db: Session, course):
        course.deleted_at = datetime.now()
        db.commit()
