from pkg.repositories import course_members as course_members_repositories


def course_members(course_id: int):
    return course_members_repositories.course_members(course_id)


def add_course_member(course_id: int, member_id: int):
    return course_members_repositories.add_course_members(course_id, member_id)


def delete_course_member(course_id: int, member_id: int):
    return course_members_repositories.delete_course_member(course_id, member_id)


