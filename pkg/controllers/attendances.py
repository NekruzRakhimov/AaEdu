import json

from fastapi import APIRouter, status, Depends

from starlette.responses import Response

from pkg.services import attendances as attendances_service

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
    attendance = attendances_service.get_attendance_by_id(user_id,attendance_id)
    response.status_code = status.HTTP_200_OK
    response.headers["Content-Type"] = "application/json"
    return attendance


@router.post("/attendances", summary="create attendance", tags=["attendances"])
def create_attendance():
    pass


@router.put("/attendances/{user_id}", summary="update attendance by id", tags=["attendances"])
def update_attendance_by_id():
    pass


@router.delete("/attendances/{user_id}", summary="delete attendance by id")
def delete_attendance_by_id():
    pass
