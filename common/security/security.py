from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from common.settings.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme),):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    username = valid_token(token, settings.SECRET_KEY)
    if not username:
        raise credentials_exception

    return username


def valid_token(token: str, key: str):
    try:
        payload = decode(token, key, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            return None

    except ExpiredSignatureError:
        return None

    except DecodeError:
        return None

    return username
