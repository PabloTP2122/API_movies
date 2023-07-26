from fastapi import APIRouter

from fastapi.responses import JSONResponse

# Esquema de usuario
from schemas.user import User

# Seguridad
from utils.jwt_manager import create_token

users_router = APIRouter()


@users_router.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == "admin":
        token = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)
