from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from to_do_list.schemas.schema_generico import GenericResponse
from common.db.db import db
from utils.files import _open_file
from to_do_list.schemas.schema_users import GetUserInput, CreateUserInput
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/create_user", status_code=HTTPStatus.CREATED, response_model=GenericResponse)
def create_user(user: CreateUserInput = Depends()) -> GenericResponse:
    sql = _open_file("common/db/sql/insert_user.sql")
    base = "local"
    params = {
        "name": user.username,
        "password": user.password
    }

    try:
        resultado = db.executa(params, sql, base)

        if not resultado:
            return JSONResponse(
                status_code=HTTPStatus.NO_CONTENT,
                content={"message": "Usuário criado, mas sem retorno do banco."}
            )

        return GenericResponse(message="Usuário criado com sucesso!")

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao criar usuário: {str(e)}"
        )

@router.post("/get_user", status_code=HTTPStatus.OK, response_model=GenericResponse)
def get_user(login: GetUserInput = Depends()) -> GenericResponse:
    sql = _open_file("common/db/sql/get_users.sql")
    base = "local"
    params = {
        "userid": login.iduser
    }

    try:
        resultado = db.consulta(params, sql, base)

        if not resultado:
            return JSONResponse(
                status_code=HTTPStatus.NO_CONTENT,
                content={"message": "Nenhum usuário encontrado com esse ID."}
            )

        return GenericResponse(
            message="Usuário encontrado com sucesso!",
            data=resultado  # Supondo que você vá adicionar esse campo no schema
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao buscar usuário: {str(e)}"
        )
