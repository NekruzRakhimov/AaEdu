import json

from fastapi import APIRouter, status, Depends

from starlette.responses import Response, JSONResponse

from db.models import Attendance
from pkg.services import attendances as attendances_service
from schemas.attendance import AttendanceSchema

router = APIRouter()


@router.get("/attendances", summary="get all attendances", tags=["attendances"])
def get_all_attendances(response: Response):
    attendances = attendances_service.get_all_attendances()
    response.status_code = status.HTTP_200_OK
    response.headers["Content-Type"] = "application/json"
    return attendances


@router.get("/attendances/{attendance_id}", summary="get attendance by id", tags=["attendances"])
def get_attendance_by_id(attendance_id: int, response: Response):
    user_id = 1
    attendance = attendances_service.get_attendance_by_id(user_id, attendance_id)
    response.status_code = status.HTTP_200_OK
    response.headers["Content-Type"] = "application/json"
    return attendance


@router.post("/attendances", summary="create attendance", tags=["attendances"])
def create_attendance(attendance: AttendanceSchema, response: Response):
    attendances_service.create_attendance(attendance)
    return JSONResponse({"message": "Task created"}, status_code=status.HTTP_201_CREATED)


@router.put("/attendances/{attendacne_id}", summary="update attendance by id", tags=["attendances"])
def update_attendance(attendance: AttendanceSchema):
    user_id = 1
    attendances_service.update_attendance(user_id, attendance)
    return JSONResponse({"message": "attendance updated"}, status_code=status.HTTP_200_OK)


@router.delete("/attendances/{attendacne_id}}", summary="delete attendance by id", tags=["attendances"])
def delete_attendance_by_id(attendance_id: int):
    user_id = 1
    attendances_service.delete_attendance(user_id, attendance_id)
    return JSONResponse({"message": "attendance deleted"})
