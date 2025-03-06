from pkg.repositories import role as role_repository
from schemas.role import RoleSchema


def get_all_roles():
    return role_repository.get_all_roles()


def create_role(role: RoleSchema):
    return role_repository.create_role(role.name)


def assign_role_to_user(user_id: int, role_id: int):
    return role_repository.assign_role_to_user(user_id, role_id)


def soft_delete_role(role_id: int):
    return role_repository.soft_delete_role(role_id)


def hard_delete_role(role_id: int):
    return role_repository.hard_delete_role(role_id)
