from fastapi import Depends, FastAPI, Body, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security.http import HTTPAuthorizationCredentials 
# Para crear esquemas
from pydantic import BaseModel, Field
# Ayuda a colocar valores opcionales
from typing import Optional, List
# Para manejo de excepciones y códigos de estado
from fastapi.exceptions import HTTPException
from starlette.requests import Request
# Base de datos
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

# Seguridad
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

#
Base.metadata.create_all(bind=engine)

# Instancia de fast api
app = FastAPI()

# Título de la documentación de la API
app.title = 'Movies API'
app.version = '0.0.1'

# Clase para procesar la petición del usuario y devolver las credenciales de autorización
# super da acceso a la clase de la que hereda
class JWTBarer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail='Credenciales no válidas')

# Nuevo modelo para la información del usuario
class User(BaseModel):
    email: str
    password: str

# La clase hereda de BaseModel para crear un esquema
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=6, max_length=55)
    overview: str = Field(min_length=16, max_length=55)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10.0)
    category: str = Field(min_length=5, max_length=16)

    # Ayuda a crear los valores por defecto en forma de diccionario
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Título",
                "overview": "Describe la película",
                "year": 2022,
                "rating": 5.0,
                "category": "categoría"
            }

        }



movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }
]

@app.exception_handler(404)
async def not_found_exception(request: Request, exc: HTTPException):
    return RedirectResponse('/404')

@app.get('/404', tags=['404'])
def not_founded():
    return HTMLResponse('<h1>Error: 404</h1>')

@app.get('/', tags=['home'],response_class=HTMLResponse)
def message():
    return HTMLResponse('<h1>Hello my friends!</h1>')


@app.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == "admin":
        token = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBarer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


#Parametros de la ruta
@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message":"No se encontró"})
    #Filtrado
    """ for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=200, content=item) """
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

#Parametros query
@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={"message":"No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    #return [movie for movie in movies if movie['category'] == category]


# Método POST para crear
@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    # Primero hay que crear sesión para conectarse a la base de datos
    db = Session()
    # creada una película
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    ##movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha reguistrado correctamente la película"}) 

# Método PUT para modificar
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200, content={"message": f"Se modificó correctamente la película con id:  {id}"})



# Método DELETE
@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return JSONResponse(status_code=200, content={"message":"Se eliminó la película"})
    