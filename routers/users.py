from fastapi import APIRouter
# Para crear esquemas
from pydantic import BaseModel

from fastapi.responses import JSONResponse

# Seguridad
from jwt_manager import create_token

users_router = APIRouter()

# Nuevo modelo para la información del usuario


class User(BaseModel):
    email: str
    password: str


@users_router.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == "admin":
        token = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)
