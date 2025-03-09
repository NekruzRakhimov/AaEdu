from sqlalchemy.orm import Session
from db.models import CourseUser

def get_course_users(course_id: int, db: Session):
    return db.query(CourseUser).filter(CourseUser.course_id == course_id).all()

def add_user_to_course(course_id: int, user_data, db: Session):
    new_entry = CourseUser(course_id=course_id, **user_data.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def remove_user_from_course(course_id: int, user_id: int, db: Session):
    entry = db.query(CourseUser).filter(CourseUser.course_id == course_id, CourseUser.user_id == user_id).first()
    if not entry:
        return None
    db.delete(entry)
    db.commit()
    return entry
