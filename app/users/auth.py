from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import EmailStr
from app.users.dao import UsersDAO
from app.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({
        'exp': expire,
        'sub': str(data.get('sub'))  # Преобразуем в строку
    })
    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITM  # Проверить правильное название
    )
    return encode_jwt



async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    if user:
        return user