import bcrypt
from pathlib import Path

# pip install bcrypt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Проверяет соответствие введённого пароля его хешу из БД """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def hash_filename(filename: str) -> str:
    salt = bcrypt.gensalt()
    filestem = Path(filename).stem
    file_extension = Path(filename).suffix
    hashed_filestem = bcrypt.hashpw(filestem.encode('utf-8'), salt).hex()
    hashed_filename = f"{hashed_filestem}{file_extension}"
    return hashed_filename