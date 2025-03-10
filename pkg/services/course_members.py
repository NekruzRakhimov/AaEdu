from pkg.repositories import course_members as course_members_repositories


def course_members(course_id: int):
    return course_members_repositories.course_members(course_id)


def add_course_member(course_id: int, member_id: int, user_id: int):
    user_role = course_members_repositories.get_user_role(user_id)
    if user_role in ['admin', 'mentor'] or user_id == member_id:
        return course_members_repositories.add_course_members(course_id, member_id)
    return False


def delete_course_member(course_id: int, member_id: int, user_id: int):
    user_role = course_members_repositories.get_user_role(user_id)
    if user_role in ['admin', 'mentor'] or user_id == member_id:
        return course_members_repositories.delete_course_member(course_id, member_id)
    return False
