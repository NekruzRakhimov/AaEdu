import json

from fastapi import APIRouter, status, Depends


router = APIRouter()


@router.get("/curs-members", summary="Get all curs members", tags=["members"])
def curs_members(course_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.user_id
    members = curs_members_services.curs_members(user_id, course_id)
    return members


@router.post("/curs-members", summary="Add member to curs", tags=["members"])
def ad_to_curse_member(payload: TokenPayload = Depends(get_current_user)):
    member_id = curs_member_services.ad_to_curse_member()
    return {
        "message": "member added successfully"
    }


@router.delete("/curs-members", summary="Delete member from curs", tags=["members"])
def del_from_curse_member(payload: TokenPayload = Depends(get_current_user)):
    member_id = curs_member_services.delete_from_course()
    return {
        "message": "member deleted successfully"
    }
