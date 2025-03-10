#### LMS (CRM) - aa.edu
Описание: Платформа для управления образовательным учреждением

#### Основные сущности
Пользователь - User
id - int (unique)
username - string
fullname - string
birth_date - time

Курс - Сourses
id - int(unique)
price - int
name - str

Урока - Lessons
id - int(unique)
title - str
description -str
course_id -int(foreign key)

Материалы для урока - LessonMaterial
id - int(unique)
meterial_tipe - str
content - str 
lesson_id -int(foreign key)

Комментарии - Comment
id - int(unique)
content - str 
lesson_id - int(foreign key)
user_id - int(foreign key)

Домашняя работа - HomeWork
id - int(unique)
score - decimal
submission_date = time 
lesson_id - int(foreing key)
student_id - int(foreing key)

Посещаемость - Attendance 
id - int(unique)
attended - bool
attendance_date - time 
lesson_id - int(foreing key)
student_id - int(foreing key)


users_courses
user_id - int
course_id - int

Отношения:
users_courses.user_id -> users.id & users_courses.course_id -> courses.id

#### Основной функционал
1. Регистрация / Вход
2. Роли: ментор, ученик, админ
3. CRUD для курсов
4. CRUD для уроков
5. CRUD для расписания
6. CRUD для материалов урока
7. CRUD для оценок (домашка)
8. CRUD для посещения
9. Я как ученик, хочу видеть аналитку по своей успеваемости
10. CRUD комментарий к уроку
11. Лента событий
12. CRUD по студентам в рамках курсов

Optional:
- Напоминания о предстоящих занятиях (email)
- Логика покупки курсов
- Интеграция с PulNest для оплаты курсов

Стек: python, postgres, sqlAlchemy, jwt, fastAPI, swagger 2.0 or 3.0

##### Участники команды:
- Альминов Руслан
- Табаров Шерзод
- Саидов Абубакр
- Салихов Абубакр
- Джумаева Тарона
- Турсунов Сухроб
- Шербадалов Хусейн
- Ибрагимов Маъруф
- Рамадонов Некруз
- Шодиева Мухлиса
