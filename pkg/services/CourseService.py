from sqlalchemy.orm import Session
from pkg.repositories.CourseRepository import CourseRepository
from pkg.schemas.CourseSchemas import CourseCreate, CourseUpdate
from fastapi import HTTPException

class CourseService:
    @staticmethod
    def get_courses(db: Session):
        return CourseRepository.get_all(db)

    @staticmethod
    def get_course(db: Session, course_id: int):
        course = CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

    @staticmethod
    def create_course(db: Session, course_data: CourseCreate):
        return CourseRepository.create(db, course_data)

    @staticmethod
    def update_course(db: Session, course_id: int, course_data: CourseUpdate):
        course = CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return CourseRepository.update(db, course, course_data)

    @staticmethod
    def delete_course(db: Session, course_id: int):
        course = CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        CourseRepository.delete(db, course)
        return {"detail": "Course deleted successfully"}