import logging
from pydantic import BaseModel

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class CommentSchema(BaseModel):
    user_id: int
    content: str

    class Config:
        from_attributes = True