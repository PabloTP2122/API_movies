from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

# Para manejo de excepciones y códigos de estado
from fastapi.exceptions import HTTPException
from starlette.requests import Request
# Base de datos
from config.database import engine, Base


# Middlewares
# Manejo de errores
from middlewares.error_handler import ErrorHandler

# Routers
from routers.movies import movie_router
from routers.users import users_router


Base.metadata.create_all(bind=engine)

# Instancia de fast api
app = FastAPI()

# Título de la documentación de la API
app.title = 'Movies API'
app.version = '0.0.1'

# Se añade middleware
app.add_middleware(ErrorHandler)

# Se añaden routers
app.include_router(movie_router)
app.include_router(users_router)


@app.exception_handler(404)
async def not_found_exception(request: Request, exc: HTTPException):
    return RedirectResponse('/404')


@app.get('/404', tags=['404'])
def not_founded():
    return HTMLResponse('<h1>Error: 404</h1>')


@app.get('/', tags=['home'], response_class=HTMLResponse)
def message():
    return HTMLResponse('<h1>Hello my friends!</h1>')
