from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.models import Course
from db.postgres import get_db
from pkg.schemas.course_schemas import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])

# TODO: Все действия, требующие уровней доступа, реализуем после добавления пользователей.

@router.get("/", response_model=list[CourseResponse], summary="Получить список курсов")
def get_courses(db: Session = Depends(get_db)):
    """Возвращает список всех курсов."""
    return db.query(Course).filter(Course.deleted_at == None).all()


@router.get("/{course_id}", response_model=CourseResponse, summary="Получить курс по ID")
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Возвращает информацию о курсе по его ID."""
    course = db.query(Course).filter(Course.id == course_id, Course.deleted_at == None).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=CourseResponse, summary="Создать новый курс")
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    """Создает новый курс и возвращает его данные."""
    new_course = Course(name=course_data.name)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@router.put("/{course_id}", response_model=CourseResponse, summary="Обновить курс по ID")
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    """Обновляет данные курса по его ID."""
    course = db.query(Course).filter(Course.id == course_id, Course.deleted_at == None).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_data.name:
        course.name = course_data.name
    course.updated_at = datetime.now()
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}", summary="Удалить курс по ID")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Помечает курс как удаленный, записывая время удаления."""
    course = db.query(Course).filter(Course.id == course_id, Course.deleted_at == None).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.deleted_at = datetime.now()
    db.commit()
    return {"detail": "Course deleted successfully"}
