from db.models import Attendance
from pkg.repositories import attendances as attendances_repository


def get_all_attendances():
    attendances = attendances_repository.get_all_attendances()
    return attendances


def get_attendance_by_id(user_id, attendance_id):
    attendance = attendances_repository.get_attendance_by_id(user_id, attendance_id)
    return attendance
