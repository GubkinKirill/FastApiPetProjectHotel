from datetime import datetime
from jose import JWTError, jwt

from fastapi import Depends, Request
from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import TokenExpireException, TokenAbsentException, IncorrectTokenFormatException, UserIsNotPresentException


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    
    if not token:
        raise TokenAbsentException

    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITM
        )
        
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get('exp')

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpireException 

    user_id: str = payload.get('sub')

    if not user_id:
        raise UserIsNotPresentException
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        
        raise UserIsNotPresentException
    
    return user



