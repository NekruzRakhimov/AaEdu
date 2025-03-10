from db.models import Attendance
from pkg.repositories import attendances as attendances_repository
from schemas.attendance import AttendanceSchema


def get_all_attendances():
    attendances = attendances_repository.get_all_attendances()
    return attendances


def get_attendance_by_id(user_id, attendance_id):
    attendance = attendances_repository.get_attendance_by_id(user_id, attendance_id)
    return attendance


def create_attendance(attendance: AttendanceSchema):
    a = Attendance()
    a.user_id = attendance.user_id
    a.lesson_id = attendance.lesson_id
    a.attended = attendance.attended
    a.attendance_date = attendance.attendance_date

    return attendances_repository.create_attendance(a)


def update_attendance(user_id, attendance: AttendanceSchema):
    a = Attendance()
    a.user_id = attendance.user_id
    a.lesson_id = attendance.lesson_id
    a.attended = attendance.attended
    return attendances_repository.update_attendance(user_id, attendance)


def delete_attendance(user_id, attendance_id):
    attendance = attendances_repository.delete_attendance(user_id, attendance_id)
    return attendance
