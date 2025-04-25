from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from to_do_list.schemas.schema_generico import GenericResponse

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login', status_code=HTTPStatus.OK, response_model=GenericResponse)
def login(login: OAuth2PasswordRequestForm = Depends()):
    try:
        usuario = f'Oi {login.username}, olha sua senha ai: {login.password}'
        
        return GenericResponse(message=usuario)
    
    except HTTPException as e:
        raise e
    except ConnectionError:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="Falha ao se conectar com a base de dados")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {str(e)}")