from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from configs.config import settings

engine = create_engine(settings.database_url)


