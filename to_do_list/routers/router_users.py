from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from to_do_list.schemas.schema_generico import GenericResponse
from common.db.db import db
from utils.files import _open_file
from utils.log import setup_logging
from to_do_list.schemas.schema_users import (
    GetUserInput, CreateUserInput
)
from fastapi.responses import JSONResponse
from common.settings.login import fusers

router = APIRouter(prefix="/auth", tags=["Auth"])
log = setup_logging(log_file='logs/auth.log')

@router.post("/create_user", status_code=HTTPStatus.CREATED, response_model=GenericResponse)
def create_user(user: CreateUserInput = Depends()) -> GenericResponse:
    sql = _open_file("common/db/sql/insert_user.sql")
    base = "local"
    log.info(f"Iniciando criação de usuário: {user.username}")

    params = fusers.criar_conta(user.username, user.password, user.email)
    try:
        resultado = db.executa(params, sql, base)

        if not resultado:
            log.warning(f"Usuário {user.username} criado, mas sem retorno do banco.")
            return JSONResponse(
                status_code=HTTPStatus.NO_CONTENT,
                content={"message": "Usuário criado, mas sem retorno do banco."}
            )

        log.info(f"Usuário {user.username} criado com sucesso.")
        return GenericResponse(message="Usuário criado com sucesso!")

    except Exception as e:
        log.error(f"Erro ao criar usuário {user.username}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao criar usuário: {str(e)}"
        )

@router.post("/get_user", status_code=HTTPStatus.OK, response_model=GenericResponse)
def get_user(login: GetUserInput = Depends()) -> GenericResponse:
    sql = _open_file("common/db/sql/get_users.sql")
    base = "local"
    log.info(f"Iniciando busca de usuário com ID: {login.iduser}")

    params = {
        "userid": login.iduser
    }

    try:
        resultado = db.consulta(params, sql, base)

        if not resultado:
            log.warning(f"Nenhum usuário encontrado com ID: {login.iduser}")
            return JSONResponse(
                status_code=HTTPStatus.NO_CONTENT,
                content={"message": "Nenhum usuário encontrado com esse ID."}
            )

        log.info(f"Usuário com ID {login.iduser} encontrado com sucesso.")
        return GenericResponse(
            message="Usuário encontrado com sucesso!",
            data=resultado
        )

    except Exception as e:
        log.error(f"Erro ao buscar usuário ID {login.iduser}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao buscar usuário: {str(e)}"
        )
