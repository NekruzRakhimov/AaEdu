<<<<<<< HEAD
#### LMS (CRM) - aa.edu
Описание: Платформа для управления образовательным учреждением

#### Основные сущности
Пользователь - User
id - int (unique)
username - string
fullname - string
email - string (unique)
birth_date - time
created_at - time
updated_at - time
deleted_at - time

Курс - courses
id - int(unique)

users_courses
user_id - int
course_id - int

Отношения:
users_courses.user_id -> users.id & users_courses.course_id -> courses.id

#### Основной функционал
1. Регистрация / Вход
2. Две роли: ментор, ученик, админ
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
