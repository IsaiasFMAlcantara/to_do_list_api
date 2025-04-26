from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from to_do_list.schemas.schema_generico import GenericResponse
from to_do_list.schemas.schema_users import GetUserInput, CreateUserInput, UpdateUserInput
from common.db.db import db
from common.settings.login import fusers
from utils.files import _open_file
from utils.log import setup_logging

router = APIRouter(prefix="/auth", tags=["Auth"])
log = setup_logging(log_file='logs/auth.log')

BASE = "local"

def execute_db(sql_path: str, params: dict, method: str = "executa"):
    sql = _open_file(sql_path)
    func = getattr(db, method, None)
    
    if not func:
        log.error(f"DB method '{method}' inválido.")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro interno: método de banco inválido."
        )
    
    return func(params, sql, BASE)

@router.post("/create_user", status_code=HTTPStatus.CREATED, response_model=GenericResponse)
def create_user(user: CreateUserInput = Depends()):
    log.info(f"Iniciando criação de usuário: {user.username}")
    try:
        params = fusers.criar_conta(user.username, user.password, user.email)
        resultado = execute_db("common/db/sql/insert_user.sql", params)

        if not resultado:
            log.warning(f"Usuário {user.username} criado, mas sem retorno do banco.")
            return JSONResponse(
                status_code=HTTPStatus.NO_CONTENT,
                content={"message": "Usuário criado, mas sem retorno do banco."}
            )

        log.info(f"Usuário {user.username} criado com sucesso.")
        return GenericResponse(message="Usuário criado com sucesso!")

    except Exception as e:
        log.exception(f"Erro ao criar usuário {user.username}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao criar usuário: {str(e)}"
        )

@router.post("/update_user", status_code=HTTPStatus.OK, response_model=GenericResponse)
def update_user(user: UpdateUserInput = Depends()):
    log.info(f"Iniciando atualização de usuário ID: {user.iduser}")
    try:
        params = fusers.atualizar_informacoes(user.iduser, user.username, user.email)
        resultado = execute_db("common/db/sql/update_name_email.sql", params)

        if resultado is None:
            log.warning(f"Nenhum dado retornado ao atualizar usuário ID {user.iduser}")
            raise HTTPException(
                status_code=HTTPStatus.NO_CONTENT,
                detail="Nenhum dado retornado ao atualizar usuário."
            )

        log.info(f"Atualização concluída para usuário ID {user.iduser}")
        return GenericResponse(message="Informações alteradas com sucesso.")

    except Exception as e:
        log.exception(f"Erro ao atualizar usuário ID {user.iduser}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao atualizar usuário: {str(e)}"
        )

@router.get("/get_user", status_code=HTTPStatus.OK, response_model=GenericResponse)
def get_user(user: GetUserInput = Depends()):
    log.info(f"Iniciando busca de usuário ID: {user.iduser}")
    try:
        params = {"userid": user.iduser}
        resultado = execute_db("common/db/sql/get_users.sql", params, method="consulta")

        if not resultado:
            log.warning(f"Nenhum usuário encontrado com ID: {user.iduser}")
            return JSONResponse(
                status_code=HTTPStatus.NO_CONTENT,
                content={"message": "Nenhum usuário encontrado com esse ID."}
            )

        log.info(f"Usuário ID {user.iduser} encontrado.")
        return GenericResponse(message="Usuário encontrado com sucesso!", data=resultado)

    except Exception as e:
        log.exception(f"Erro ao buscar usuário ID {user.iduser}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao buscar usuário: {str(e)}"
        )
