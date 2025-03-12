from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from pkg.services.schedule_service import (
    fetch_schedules,
    fetch_schedule_by_id,
    add_schedule,
    modify_schedule,
    remove_schedule,
)
from schemas.schedule import ScheduleSchema
from utils.auth import get_db, get_current_user
from utils.auth import TokenPayload

router = APIRouter()


@router.get("/schedule/{course_id}", summary="Get course schedule", tags=["schedule"])
def get_schedules(course_id: int, db: Session = Depends(get_db), payload: TokenPayload = Depends(get_current_user)):
    return fetch_schedules(course_id, db)


@router.get("/schedule/item/{schedule_id}", summary="Get schedule by ID", tags=["schedule"])
def get_schedule_by_id(schedule_id: int, db: Session = Depends(get_db), payload: TokenPayload = Depends(get_current_user)):
    schedule = fetch_schedule_by_id(schedule_id, db)
    if not schedule:
        return JSONResponse({"message": "Schedule not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return schedule


@router.post("/schedule", summary="Create schedule", tags=["schedule"])
def create_schedule(
    schedule: ScheduleSchema,
    db: Session = Depends(get_db),
    payload: TokenPayload = Depends(get_current_user)
):
    if payload.role not in ["admin", "teacher"]:
        return JSONResponse({"message": "Access denied"}, status_code=status.HTTP_403_FORBIDDEN)

    add_schedule(schedule, db)
    return JSONResponse({"message": "Schedule created"}, status_code=status.HTTP_201_CREATED)


@router.put("/schedule/{schedule_id}", summary="Update schedule", tags=["schedule"])
def update_schedule(
    schedule_id: int,
    schedule: ScheduleSchema,
    db: Session = Depends(get_db),
    payload: TokenPayload = Depends(get_current_user)
):
    if payload.role not in ["admin", "teacher"]:
        return JSONResponse({"message": "Access denied"}, status_code=status.HTTP_403_FORBIDDEN)

    updated = modify_schedule(schedule_id, schedule, db)
    if not updated:
        return JSONResponse({"message": "Schedule not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({"message": "Schedule updated"}, status_code=status.HTTP_200_OK)


@router.delete("/schedule/{schedule_id}", summary="Delete schedule", tags=["schedule"])
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    payload: TokenPayload = Depends(get_current_user)
):
    if payload.role != "admin":
        return JSONResponse({"message": "Access denied"}, status_code=status.HTTP_403_FORBIDDEN)

    deleted = remove_schedule(schedule_id, db)
    if not deleted:
        return JSONResponse({"message": "Schedule not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({"message": "Schedule deleted"}, status_code=status.HTTP_204_NO_CONTENT)
