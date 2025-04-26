from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from common.settings.settings import settings
from utils.log import setup_logging

log = setup_logging(log_file='logs/security.log')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def create_access_token(data: dict):
    log.info("Iniciando criação de access token.")
    try:
        to_encode = data.copy()
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({'exp': expire})
        encoded_jwt = encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        log.info(f"Token criado com expiração em {expire.isoformat()}")
        return encoded_jwt
    except Exception as e:
        log.error(f"Erro ao criar token: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro interno ao gerar token de acesso."
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    log.info("Validando token do usuário.")
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não foi possível validar as credenciais.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    username = valid_token(token, settings.SECRET_KEY)
    if not username:
        log.warning('Token inválido ou usuário não encontrado.')
        raise credentials_exception

    log.info(f"Usuário autenticado com sucesso: {username}")
    return username

def valid_token(token: str, key: str):
    log.debug("Iniciando validação de token JWT.")
    try:
        payload = decode(token, key, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')

        if not username:
            log.warning('Token decodificado mas sem "sub" (usuário).')
            return None

        log.debug(f"Token válido para o usuário: {username}")
        return username

    except ExpiredSignatureError:
        log.error('Sessão expirada: token expirado.')
        return None

    except DecodeError:
        log.error('Erro de decodificação do token JWT.')
        return None

    except Exception as e:
        log.error(f"Erro inesperado ao validar token: {str(e)}", exc_info=True)
        return None
