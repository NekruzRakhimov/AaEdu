import json
from fastapi import APIRouter, status, HTTPException, Depends
from starlette.responses import Response

from pkg.services import event as event_service
from schemas.event import EventSchema, EventUpdateSchema
from db.models import User

router = APIRouter()


def get_current_user():
    user = User(id=3,
                full_name="Vasiliy Fedorov",
                username="vasya221",
                password="123456",
                role_id=3)
    return user


def is_admin(user: User = Depends(get_current_user)):
    if user.role_id != 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can perform this action")
    return user


@router.get("/events", summary="Get recent events", tags=["events"])
def get_recent_events():
    events = event_service.get_recent_events()
    return events


@router.post("/events", summary="Create a new event", tags=["events"])
def create_event(event: EventSchema, user: User = Depends(is_admin)):
    event_id = event_service.create_event(event, user)
    return Response(json.dumps({'message': 'Event successfully created', 'event_id': event_id}),
                    status_code=status.HTTP_201_CREATED,
                    media_type='application/json')


@router.put("/events/{event_id}")
def update_event(event_id: int, event_data: EventUpdateSchema, user: User = Depends(is_admin)):
    updated_event = event_service.update_event(event_id, event_data.new_description, user)
    if not updated_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return {"message": "Event updated successfully", "event": updated_event}


@router.delete("/events/{event_id}", summary="Soft delete an event", tags=["events"])
def soft_delete_event(event_id: int, user: User = Depends(is_admin)):
    event = event_service.soft_delete_event(event_id, user)
    if event is None:
        return Response(
            json.dumps({'error': 'Event not found'}),
            status_code=status.HTTP_404_NOT_FOUND
        )

    return Response(
        json.dumps({'message': 'Event successfully soft deleted'}),
        status_code=status.HTTP_200_OK
    )


@router.delete("/events/{event_id}/hard", summary="Hard delete an event", tags=["events"])
def hard_delete_event(event_id: int, user: User = Depends(is_admin)):
    event = event_service.hard_delete_event(event_id, user)
    if event is None:
        return Response(
            json.dumps({'error': 'Event not found'}),
            status_code=status.HTTP_404_NOT_FOUND
        )

    return Response(
        json.dumps({'message': 'Event successfully hard deleted'}),
        status_code=status.HTTP_200_OK
    )
