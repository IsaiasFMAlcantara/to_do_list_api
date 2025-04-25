from fastapi import APIRouter
from http import HTTPStatus
from to_do_list.schemas.schema_generico import GenericResponse

router = APIRouter(tags=['Home'])

@router.get('/', status_code=HTTPStatus.OK, response_model=GenericResponse, include_in_schema=False)
def root():
    return GenericResponse(message='Bem-vindo a api de dashboard de gerentes Novalar')
