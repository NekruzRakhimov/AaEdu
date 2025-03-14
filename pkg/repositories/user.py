from sqlalchemy.orm import Session

from db.postgres import engine
from db.models import User, Role


def get_all_users():
    with Session(bind=engine) as db:
        db_users = db.query(User).all()

        return db_users


def get_user_by_username(username):
    with Session(bind=engine) as db:
        db_user = db.query(User).filter(User.username == username).first()

        return db_user


def get_user_by_username_and_password(username, password):
    with Session(bind=engine) as db:
        db_user = db.query(User).filter(
            User.username == username, User.password == password).first()

        return db_user


def create_user(user: User):
    with Session(bind=engine) as db:
        db.add(user)
        db.commit()
        return user.id


def get_user_by_id(id):
    with Session(bind=engine) as db:
        db_user = db.query(User).filter(User.id == id).first()

        return db_user


def get_user_role(user_id: int):
    with Session(bind=engine) as db:
        user = db.query(User).filter(User.id == user_id).first()
        role = db.query(Role).filter(Role.id == user.role_id).first()
        return role.name
