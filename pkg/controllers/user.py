import json
from fastapi import APIRouter, status, Depends
from starlette.responses import Response

from pkg.controllers.middlewares import get_current_user
from pkg.services import user as user_service
from utils.auth import TokenPayload

router = APIRouter()


@router.get("/users")
def get_users(payload: TokenPayload = Depends(get_current_user)):
    if payload.role != "admin":
        return Response(json.dumps({"error": "only admin can get list of users"}),
                        status_code=status.HTTP_403_FORBIDDEN)

    users = user_service.get_all_users()
    return users
