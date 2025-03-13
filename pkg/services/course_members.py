from pkg.repositories import course_members as course_members_repositories
from pkg.repositories import CourseRepository
from pkg.repositories import user


def course_members(course_id: int):
    return course_members_repositories.course_members(course_id)


def add_course_member(course_id: int, member_id: int, user_id: int):
    if not user.get_user_by_id(member_id):
        return {
            "message": "There is no user with such id"
        }
    user_role = user.get_user_role(user_id)
    if not (user_role in ['admin', 'mentor'] or user_id == member_id):
        return {
            "message": "Only admins or mentors are allowed to add member to the course. You can add only yourself to the course"
        }
    if course_members_repositories.get_course_members_by_member_id(course_id, member_id):
        return {
            "message": "Member already in this course"
        }

    course_members_repositories.add_course_members(course_id, member_id)
    return {
        "message": "You added member to the course"
    }


def delete_course_member(course_id: int, member_id: int, user_id: int):
    user_role = user.get_user_role(user_id)
    if user_role in ['admin', 'mentor'] or user_id == member_id:
        return course_members_repositories.delete_course_member(course_id, member_id)
    return False
