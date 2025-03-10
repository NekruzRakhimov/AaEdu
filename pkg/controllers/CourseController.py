from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.postgres import get_db
from pkg.services.CourseService import CourseService
from pkg.schemas.CourseSchemas import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=list[CourseResponse], summary="Получить список курсов")
def get_courses(db: Session = Depends(get_db)):
    """Возвращает список всех курсов."""
    return CourseService.get_courses(db)

@router.get("/{course_id}", response_model=CourseResponse, summary="Получить курс по ID")
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Возвращает информацию о курсе по его ID."""
    return CourseService.get_course(db, course_id)

@router.post("/", response_model=CourseResponse, summary="Создать новый курс")
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    """Создает новый курс и возвращает его данные."""
    return CourseService.create_course(db, course_data)

@router.put("/{course_id}", response_model=CourseResponse, summary="Обновить курс по ID")
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    """Обновляет данные курса по его ID."""
    return CourseService.update_course(db, course_id, course_data)

@router.delete("/{couse_id}", summary="Удалить курс по ID")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Помечает курс как удаленный, записывая время удаления."""
    return CourseService.delete_course(db, course_id)