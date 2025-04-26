from pydantic import BaseModel

class GetUserInput(BaseModel):
    iduser: int

class CreateUserInput(BaseModel):
    username: str
    password: str