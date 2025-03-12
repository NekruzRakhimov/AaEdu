from fastapi import APIRouter, status, Depends
from starlette.responses import Response, JSONResponse
from pkg.controllers.middlewares import get_current_user
from pkg.repository import schedule as schedule_repository
from pkg.schemas.schedule import ScheduleCreate, ScheduleUpdate
from utils.auth import TokenPayload

router = APIRouter()


# Получение расписания курса (уровень доступа: ментор, студент)
@router.get("/schedule/{course_id}", summary="Get all schedules", tags=["schedule"])
def get_all_schedules(course_id: int, payload: TokenPayload = Depends(get_current_user)):
    # TODO: check role

    schedules = schedule_repository.get_schedules(course_id)
    return schedules


# Получение расписания по ID (уровень доступа: ментор, студент)
@router.get("/schedule/{course_id}/{schedule_id}", summary="Get schedule by ID", tags=["schedule"])
def get_schedule_by_id(course_id: int, schedule_id: int, payload: TokenPayload = Depends(get_current_user)):
    # TODO: check role

    schedule = schedule_repository.create_schedule(course_id, schedule)
    if schedule is None:
        return JSONResponse({"message": "Schedule not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return schedule


# Создание расписания (уровень доступа: ментор)
@router.post("/schedule/{course_id}", summary="Create new schedule", tags=["schedule"])
def create_schedule(course_id: int, schedule: ScheduleCreate, payload: TokenPayload = Depends(get_current_user)):
    schedule_repository.create_schedule(course_id, schedule)

    return JSONResponse({"message": "Schedule created"}, status_code=status.HTTP_201_CREATED)


# Обновление расписания (уровень доступа: ментор)
@router.put("/schedule/{course_id}/{schedule_id}", summary="Update schedule", tags=["schedule"])
def update_schedule(course_id: int, schedule_id: int, schedule: ScheduleUpdate, payload: TokenPayload = Depends(get_current_user)):

    updated_schedule = schedule_repository.update_schedule(course_id, schedule_id, schedule)
    if updated_schedule is None:
        return JSONResponse({"message": "Schedule not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse({"message": "Schedule updated"}, status_code=status.HTTP_200_OK)


# Удаление расписания (уровень доступа: ментор)
@router.delete("/schedule/{course_id}/{schedule_id}", summary="Delete schedule", tags=["schedule"])
def delete_schedule(course_id: int, schedule_id: int, payload: TokenPayload = Depends(get_current_user)):
    # TODO: check role

    deleted_schedule = schedule_repository.delete_schedule(course_id, schedule_id)
    if deleted_schedule is None:
        return JSONResponse({"message": "Schedule not found"}, status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)