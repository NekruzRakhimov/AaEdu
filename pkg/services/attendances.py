from db.models import Attendance
from pkg.repositories import attendances as attendances_repository
from schemas.attendance import AttendanceSchema


def get_all_attendances():
    attendances = attendances_repository.get_all_attendances()
    return attendances


def get_attendance_by_id(user_id, attendance_id):
    attendance = attendances_repository.get_attendance_by_id(user_id, attendance_id)
    return attendance


def create_attendance(role_id, attendance: AttendanceSchema):
    if role_id == 1:
        return "you are not allowed to create attendance"

    a = Attendance()
    a.user_id = attendance.user_id
    a.lesson_id = attendance.lesson_id
    a.course_id = attendance.course_id
    return attendances_repository.create_attendance(a)


def update_attendance(role_id, attendance: AttendanceSchema):
    if role_id == 1:
        return "You are not allowed to update attendance"
    a = Attendance()
    a.user_id = attendance.user_id
    a.lesson_id = attendance.lesson_id
    a.attended = attendance.attended
    return attendances_repository.update_attendance(attendance)


def delete_attendance(role_id, attendance_id):
    if role_id == 1:
        return "You are not allowed to delete attendance"
    attendance = attendances_repository.delete_attendance(attendance_id)
    return attendance
