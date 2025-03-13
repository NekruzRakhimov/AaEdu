import datetime

from pkg.repositories import CourseRepository
from db.models import Course as CourseModel
from schemas.CourseSchemas import CourseSchema
from pkg.services import user


def get_courses():
    return CourseRepository.get_all()


def create_course(user_id, course_schema: CourseSchema):
    user_permission = user.admin_or_mentor_permission_check(user_id)
    if user_permission:
        return user_permission
    course = CourseModel()
    course.name = course_schema.name
    course.description = course_schema.description
    course.price = course_schema.price
    course.created_at = datetime.datetime.now()
    course.updated_at = datetime.datetime.now()
    return CourseRepository.create(course)


def update_course(user_id, course_schema: CourseSchema, course_id: int):
    user_permission = user.admin_or_mentor_permission_check(user_id)
    if user_permission:
        return user_permission
    if not CourseRepository.get_by_id(course_id):
        return {
            "message": "Course not exist"
        }
    course = CourseModel()
    course.id = course_id
    course.name = course_schema.name
    course.description = course_schema.description
    course.price = course_schema.price
    course.created_at = datetime.datetime.now()
    course.updated_at = datetime.datetime.now()
    return CourseRepository.update(course)


def delete_course(user_id: int, course_id):
    user_permission = user.admin_or_mentor_permission_check(user_id)
    if user_permission:
        return user_permission
    if not CourseRepository.get_by_id(course_id):
        return {
            "message": "Course not exist"
        }
    return CourseRepository.delete(course_id)