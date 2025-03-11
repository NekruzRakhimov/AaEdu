from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import sessionmaker

from configs.config import settings

engine = create_engine(settings.database_url)


def get_db():
    return None
