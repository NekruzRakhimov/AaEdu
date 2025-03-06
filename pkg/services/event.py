from fastapi import HTTPException
from starlette import status

from db.models import Event, User
from pkg.repositories import event as event_repository
from schemas.event import EventSchema


def get_recent_events():
    return event_repository.get_recent_events()


def create_event(event: EventSchema, user: User):
    e = Event()
    e.user_id = user.id
    e.event_type = event.event_type
    e.event_description = event.event_description
    e.related_id = event.related_id

    return event_repository.create_event(e)


def update_event(event_id: int, new_description: str, user: User):
    if user.role_id != 3:
        raise PermissionError("Only admins can delete events")

    return event_repository.update_event(event_id, new_description)


def soft_delete_event(event_id: int, user: User):
    if user.role_id != 3:
        raise PermissionError("Only admins can delete events")

    return event_repository.soft_delete_event(event_id)


def hard_delete_event(event_id: int, user: User):
    if user.role_id != 3:
        raise PermissionError("Only admins can delete events")

    return event_repository.hard_delete_event(event_id)
