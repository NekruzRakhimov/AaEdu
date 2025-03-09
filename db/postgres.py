from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs.config import settings

engine = create_engine(settings.database_url)

# Создание фабрики сессий

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция получения сессии базы данных

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
