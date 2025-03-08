import json

from fastapi import APIRouter, status, Depends

from pkg.controllers.middlewares import get_current_user
from pkg.services import course_members as course_members_services
from utils.auth import TokenPayload

router = APIRouter()


@router.get("/course-members/{course_id}", summary="Get all course members", tags=["members"])
def course_members(course_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.user_id
    members = course_members_services.course_members(course_id)
    return members


@router.post("/course-members/{course_id}", summary="Add member to course", tags=["members"])
def add_member_to_course(payload: TokenPayload = Depends(get_current_user)):
    member_id = course_members_services.add_member_to_coursee()
    return {
        "message": "member added successfully"
    }


@router.delete("/course-members/{course_id}", summary="Delete member from course", tags=["members"])
def del_from_course_member(payload: TokenPayload = Depends(get_current_user)):
    member_id = course_members_services.delete_from_course()
    return {
        "message": "member deleted successfully"
    }
