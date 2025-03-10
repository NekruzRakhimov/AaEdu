from fastapi import APIRouter, Depends
from schemas.course_members import CourseMembers
from pkg.services import course_members as course_members_service
from pkg.controllers.middlewares import get_current_user
from utils.auth import TokenPayload

router = APIRouter(prefix='/course-members', tags=['course_members'])


@router.get("/{course_id}", summary="Get all course members")
def course_members(course_id: int):
    members = course_members_service.course_members(course_id)
    return {'members': members}

@router.post("/{course_id}", summary="Add member to course")
def add_course_member(course_id: int, course_member: CourseMembers, payload: TokenPayload = Depends(get_current_user)):
    member_id = course_member.member_id
    user_id = payload.id
    result = course_members_service.add_course_member(course_id, member_id, user_id)
    if result:
        return {'message': 'You added member successfully'}
    return {'message': 'Only admin or mentor can add another user'}


@router.delete("/{course_id}", summary="Delete member from course")
def delete_course_member(course_id: int, course_member: CourseMembers, payload: TokenPayload = Depends(get_current_user)):
    member_id = course_member.member_id
    user_id = payload.id
    result = course_members_service.delete_course_member(course_id, member_id, user_id)
    if result:
        return {'message': 'Member deleted successfully'}
    return {'message': 'Only admin or mentor can delete another user'}


