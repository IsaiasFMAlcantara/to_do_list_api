from pydantic import BaseModel
from typing import Optional

class GetUserInput(BaseModel):
    iduser: int

class CreateUserInput(BaseModel):
    username: str
    email: str
    password: str

class UpdateUserInput(BaseModel):
    iduser: int
    username: Optional[str] = None
    email: Optional[str] = None