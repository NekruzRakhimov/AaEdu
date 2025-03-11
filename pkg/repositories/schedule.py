from sqlalchemy.orm import Session
from db.models import Schedule


def get_schedules(course_id: int, db: Session):
    return db.query(Schedule).filter(Schedule.course_id == course_id).all()


def get_schedule_by_id(course_id: int, schedule_id: int, db: Session):
    return db.query(Schedule).filter(Schedule.course_id == course_id, Schedule.id == schedule_id).first()


def create_schedule(course_id: int, schedule_data, db: Session):
    new_schedule = Schedule(course_id=course_id, **schedule_data.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule


def update_schedule(course_id: int, schedule_id: int, schedule_data, db: Session):
    schedule = get_schedule_by_id(course_id, schedule_id, db)
    if not schedule:
        return None
    schedule.scheduled_time = schedule_data.scheduled_time
    db.commit()
    return schedule


def delete_schedule(course_id: int, schedule_id: int, db: Session):
    schedule = get_schedule_by_id(course_id, schedule_id, db)
    if not schedule:
        return None
    db.delete(schedule)
    db.commit()
    return schedule
