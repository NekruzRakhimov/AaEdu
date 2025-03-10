from db.models import CourseUser, User
from sqlalchemy.orm import Session

from db.postgres import engine


def course_members(course_id):
    with Session(bind=engine) as db:
        members = db.query(User).join(CourseUser).filter(CourseUser.course_id == course_id).all()
        members_list = []
        for member in members:
            members_list.append(member.full_name)

        return members_list


def add_course_members(course_id: int, member_id: int):
    with Session(bind=engine) as db:
        db.add(CourseUser(course_id=course_id, user_id=member_id))
        db.commit()


def delete_course_members(course_id: int, member_id: int):
    with Session(bind=engine) as db:
        db.delete(CourseUser(course_id=course_id, user_id=member_id))
        db.commit()