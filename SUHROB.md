Управление студентами – карточки студентов с личными данными, академическими показателями, оплатами и посещаемостью.
Управление преподавателями – расписание, нагрузка, рейтинг, успеваемость студентов, комментарии.
Электронный дневник и журнал – выставление оценок, комментарии преподавателей, статистика.
Личный кабинет – для студентов, родителей, преподавателей и администрации.
Учебные материалы и тестирование – возможность загружать материалы, проводить тестирования и экзамены онлайн.




-- Таблицы: 
User
user_id - int (unique)
username - string
full_name - string
birth_date - time
created_at - time
updated_at - time
deleted_at - time
passwords - string (unique)


Role
role_id - int (unique)
name - string (unique)
created_at - time
updated_at - time
deleted_at - time


Course
course_id - int (unique)
name - string
price - int
created_at - time
updated_at - time
deleted_at - time

Lesson
Course id 
lesson_id - int (unique)
tittle - string 
description - string
content - string
created_at - time
updated_at - time
deleted_at - time


Homework
id lesson
id student
scorpe


Журнал посещении

Лента событий

Расписании

