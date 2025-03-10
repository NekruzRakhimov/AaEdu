from fastapi import APIRouter, Depends
from schemas.course_members import CourseMembers
from pkg.services import course_members as course_members_service

router = APIRouter(prefix='/course_members', tags=['course_members'])


@router.get("/{course_id}", summary="Get all course members")
def course_members(course_id: int):
    members = course_members_service.course_members(course_id)
    return {'members': members}


@router.post("/{course_id}", summary="Get all course members")
def add_course_member(course_id: int, user_id: CourseMembers):
    member_id = user_id.member_id
    course_members_service.add_course_member(course_id, member_id)
    return {
        "message": "successfully added to course"
    }


@router.delete("/{course_id}", summary="Delete member from course")
def delete_course_member(course_id: int, user_id:CourseMembers):
    member_id = user_id.member_id
    course_members_service.delete_course_member(course_id, member_id)
    return {
        "message": "successfully deleted from course"
    }