from sqlalchemy.orm import Session
from pkg.repositories.schedule_repository import (
    get_schedules,
    get_schedule_by_id,
    create_schedule,
    update_schedule,
    delete_schedule,
)
from schemas.schedule import ScheduleSchema


def fetch_schedules(course_id: int, db: Session):
    return get_schedules(course_id, db)


def fetch_schedule_by_id(schedule_id: int, db: Session):
    return get_schedule_by_id(schedule_id, db)


def add_schedule(schedule: ScheduleSchema, db: Session):
    return create_schedule(schedule, db)


def modify_schedule(schedule_id: int, schedule: ScheduleSchema, db: Session):
    return update_schedule(schedule_id, schedule, db)


def remove_schedule(schedule_id: int, db: Session):
    return delete_schedule(schedule_id, db)
