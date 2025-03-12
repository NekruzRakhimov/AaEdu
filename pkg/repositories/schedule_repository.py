from sqlalchemy.orm import Session
from pkg.models.schedule import Schedule


def get_schedules(course_id: int, db: Session):
    return db.query(Schedule).filter(Schedule.course_id == course_id).all()


def get_schedule_by_id(schedule_id: int, db: Session):
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def create_schedule(schedule, db: Session):
    new_schedule = Schedule(**schedule.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule


def update_schedule(schedule_id: int, schedule, db: Session):
    existing_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not existing_schedule:
        return None
    for key, value in schedule.dict().items():
        setattr(existing_schedule, key, value)
    db.commit()
    db.refresh(existing_schedule)
    return existing_schedule


def delete_schedule(schedule_id: int, db: Session):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        return None
    db.delete(schedule)
    db.commit()
    return schedule
