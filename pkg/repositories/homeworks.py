from sqlalchemy.orm import Session
from db.models import Homework
from typing import List, Optional

def create_homework(session: Session, lesson_id: int, student_id: int, score: float) -> Homework:
    homework = Homework(lesson_id=lesson_id, student_id=student_id, score=score)
    session.add(homework)
    session.commit()
    session.refresh(homework)
    return homework

def get_homework_by_id(session: Session, homework_id: int) -> Optional[Homework]:
    return session.query(Homework).filter(Homework.id == homework_id).first()

def get_homeworks_by_student(session: Session, student_id: int) -> List[Homework]:
    return session.query(Homework).filter(Homework.student_id == student_id).all()

def update_homework(session: Session, homework_id: int, score: float) -> Optional[Homework]:
    homework = session.query(Homework).filter(Homework.id == homework_id).first()
    if homework:
        homework.score = score
        session.commit()
        session.refresh(homework)
    return homework

def delete_homework(session: Session, homework_id: int) -> bool:
    homework = session.query(Homework).filter(Homework.id == homework_id).first()
    if homework:
        session.delete(homework)
        session.commit()
        return True
    return False
