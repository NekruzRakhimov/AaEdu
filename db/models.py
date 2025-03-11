import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, DECIMAL, MetaData
from sqlalchemy.schema import CreateSchema

from db.postgres import engine

schema_name = 'aa_edu'
metadata = MetaData(schema=schema_name)


class Base(DeclarativeBase):
    metadata = metadata


# Таблица пользователей (студенты, родители, преподаватели, администраторы)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)   # Полное имя
    # Логин пользователя
    username = Column(String, unique=True, nullable=False)
    # Пароль (должен быть хеширован)
    password = Column(String, unique=True, nullable=False)
    birth_date = Column(DateTime)  # Дата рождения
    # ID роли (Один пользователь - одна роль)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    # Дата создания аккаунта
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)  # Дата обновления
    # Дата удаления (если пользователь был удален)
    deleted_at = Column(DateTime, nullable=True)


# Таблица ролей (Студент, Преподаватель, Администратор, Родитель)
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # Название роли
    created_at = Column(
        DateTime, default=datetime.datetime.now)  # Дата создания
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)  # Дата обновления
    deleted_at = Column(DateTime, nullable=True)  # Дата удаления


# Таблица курсов (каждый курс может содержать несколько уроков)
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название курса
    price = Column(Integer)  # Стоимость курса
    created_at = Column(
        DateTime, default=datetime.datetime.now)   # Дата создания
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)  # Дата обновления
    deleted_at = Column(DateTime, nullable=True)  # Дата удаления


# Таблица связи пользователей и курсов (многие ко многим: кто записан на курс)
class CourseUser(Base):
    __tablename__ = "course_users"
    course_id = Column(Integer, ForeignKey("courses.id"),
                       primary_key=True)  # ID курса
    user_id = Column(Integer, ForeignKey("users.id"),
                     primary_key=True)  # ID пользователя


# Таблица уроков (содержит информацию об уроках внутри курса)
class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    # ID курса, к которому принадлежит урок
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String, nullable=False)  # Название урока
    description = Column(Text)  # Описание урока
    created_at = Column(
        DateTime, default=datetime.datetime.now)   # Дата создания
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)  # Дата обновления
    deleted_at = Column(DateTime, nullable=True)   # Дата удаления


# Таблица материалов для уроков
class LessonMaterial(Base):
    __tablename__ = "lesson_materials"
    id = Column(Integer, primary_key=True)
    # ID урока, к которому принадлежит материал
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    filename = Column(String)  # имя файла
    hashed_filename = Column(String)  # хэшированное имя файла
    file_size_bytes = Column(Integer)  # размер файла
    created_at = Column(
        DateTime, default=datetime.datetime.now)  # Двта создания
    # Дата обновления
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)  # Дата удаления


# Таблица комментариев к урокам
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    # ID урока, к которому принадлежит коммент
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    # ID пользователя, к которому принадлежит коммент
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)  # Текст комментария
    created_at = Column(
        DateTime, default=datetime.datetime.now)  # Двта создания
    # updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # Дата обновления
    # deleted_at = Column(DateTime, nullable=True)  # Дата удаления


# Таблица домашних заданий (содержит оценки за выполненные задания)
class Homework(Base):
    tablename = "homeworks"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))  # ID урока
    student_id = Column(Integer, ForeignKey("users.id"))  # ID студента
    course_id = Column(Integer, ForeignKey("courses.id"))
    score = Column(DECIMAL(5, 2))  # Оценка за задание (0.00 - 100.00)
    submission_date = Column(DateTime, default=datetime.datetime.now)
    mentor_id = Column(Integer, ForeignKey("users.id"))
    deleted_at = Column(DateTime, nullable=True, default=None)



class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))  # ID урока
    student_id = Column(Integer, ForeignKey("users.id"))  # ID студента
    # Был ли студент на занятии (True = Да, False = Нет)
    attended = Column(Boolean)
    attendance_date = Column(
        DateTime, default=datetime.datetime.now)  # Дата посещения


# Аналитика успеваемости студента
class StudentPerformance(Base):
    __tablename__ = "student_performances"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"))  # ID студента
    course_id = Column(Integer, ForeignKey("courses.id"))  # ID курса
    avg_score = Column(DECIMAL(5, 2))  # Средний балл (0.00 - 100.00)
    # Процент посещаемости (0.00 - 100.00)
    attendance_rate = Column(DECIMAL(5, 2))


# Лента событий (лог действий: обновления оценок, новые уроки и т. д.) - *** only admin ***
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    # ID пользователя, связанного с событием
    user_id = Column(Integer, ForeignKey("users.id"))
    # Тип события ('обновление оценки', 'новый урок')
    event_type = Column(String)
    event_description = Column(Text)  # Описание события
    # ID связанного объекта (урока, курса, комментария и т. д.)
    related_id = Column(Integer)
    created_at = Column(
        DateTime, default=datetime.datetime.now)  # Дата события
    updated_at = Column(DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now)  # Дата обновления
    deleted_at = Column(DateTime, nullable=True)  # Дата удаления
    # Только администратор может редактировать
    only_admin_editable = Column(Boolean, default=True)


# Таблица расписания (расписание занятий для студентов и преподавателей)
class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))  # ID курса
    lesson_id = Column(Integer, ForeignKey("lessons.id"))  # ID урока
    teacher_id = Column(Integer, ForeignKey("users.id"))  # ID преподавателя
    scheduled_time = Column(DateTime, nullable=False)  # Дата и время занятия


def create_schema():
    try:
        with engine.connect() as connection:
            connection.execute(CreateSchema(schema_name, if_not_exists=True))
            connection.commit()
    except Exception as e:
        print(f"Ошибка во время создания схемы: {e}")


def migrate_tables():
    try:
        create_schema()
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Ошибка во время миграции: {e}")
