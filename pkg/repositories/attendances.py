from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Attendance


def get_all_attendances():
    with Session(bind=engine) as db:
        db_attendances = db.query(Attendance).all()
        attendances = list()
        for attendance in db_attendances:
            a = Attendance()
            a.user_id = attendance.user_id
            a.lesson_id = attendance.lesson_id
            a.course_id = attendance.course_id
            a.attended = attendance.attended
            a.attendance_date = attendance.attendance_date
            attendances.append(a)
        return attendances


def get_attendance_by_id(user_id, attendance_id):
    with Session(bind=engine) as db:
        db_attendances = db.query(Attendance).filter(Attendance.user_id == user_id,
                                                     Attendance.id == attendance_id).first()
        if db_attendances is None:
            return None
        attendance = Attendance()
        attendance.user_id = db_attendances.user_id
        attendance.lesson_id = db_attendances.lesson_id
        attendance.course_id = db_attendances.course_id
        attendance.attended = db_attendances.attended
        attendance.attendance_date = db_attendances.attendance_date
        return attendance


def create_attendance(attendance: Attendance):
    with Session(bind=engine) as db:
        attendance_db = Attendance(user_id=attendance.user_id,
                                   lesson_id=attendance.lesson_id,
                                   course_id=attendance.course_id,
                                   attended=attendance.attended,
                                   attendance_date=attendance.attendance_date)
        db.add(attendance_db)
        db.commit()
        return attendance_db.id


def update_attendance(user_id, attendance):
    with Session(bind=engine) as db:
        attendance_db = db.query(Attendance).filter(Attendance.id == attendance.id,
                                                    Attendance.user_id == user_id).first()
        attendance_db.user_id = attendance.user_id
        attendance_db.lesson_id = attendance.lesson_id
        attendance_db.course_id = attendance.course_id
        attendance_db.attended = attendance.attended
        db.commit()


def delete_attendance(user_id, attendance_id):
    with Session(bind=engine) as db:
        attendance_db = db.query(Attendance).filter(Attendance.id == attendance_id,
                                                    Attendance.user_id == user_id).first()
        db.delete(attendance_db)
        db.commit()

