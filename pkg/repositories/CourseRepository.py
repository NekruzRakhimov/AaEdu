import datetime

from sqlalchemy.orm import Session
from db.models import Course as CourseModel
from db.postgres import engine


def get_all():
    with Session(bind=engine) as db:
        course_models_list = db.query(CourseModel).filter(CourseModel.deleted_at == None).all()
        course_list = []
        for course in course_models_list:
            print(course.name)
            course_list.append(course.name)
        return course_list


def get_by_id(course_id: int):
    with Session(bind=engine) as db:
        return db.query(CourseModel).filter(CourseModel.id == course_id, CourseModel.deleted_at == None).first()


def create(course: CourseModel):
    with Session(bind=engine) as db:
        new_course = CourseModel(name=course.name,
                                 description=course.description,
                                 price=course.price)
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return {
            "message": f"course {new_course.name}  created successfully"
        }


def update(updated_course: CourseModel):
    with Session(bind=engine) as db:
        course_to_be_update = db.query(CourseModel).filter(CourseModel.id == updated_course.id).first()
        course_to_be_update.name = updated_course.name
        course_to_be_update.price = updated_course.price
        course_to_be_update.description = updated_course.description
        course_to_be_update.updated_at = datetime.datetime.now()
        db.commit()
        db.refresh(course_to_be_update)
        return {
            "message": f"course updated  successfully"
        }


def delete(course_id: int):
    with Session(bind=engine) as db:
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        course.deleted_at = datetime.datetime.now()
        db.commit()
        db.refresh(course)

        return {
            "message": "Course deleted successfully"
        }
