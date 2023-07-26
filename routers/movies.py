from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse

# Ayuda a colocar valores opcionales
from typing import List
# Base de datos
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

# Esquema de Movie
from schemas.movie import Movie

# Manejo de JWT
from middlewares.jwt_bearer import JWTBarer
# Servicio con la lógica
from services.movie import MovieService

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBarer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# Parametros de la ruta
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró"})
    # Filtrado
    """ for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=200, content=item) """
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Parametros query


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    # return [movie for movie in movies if movie['category'] == category]


# Método POST para crear una película
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    # Primero hay que crear sesión para conectarse a la base de datos
    db = Session()
    # creada una película
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha reguistrado correctamente la película"})

# Método PUT para modificar


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": f"No se encontró la película con id:  {id}"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": f"Se modificó correctamente la película con id:  {id}"})


# Método DELETE
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": f"No se encontró la película con id:  {id}"})
    MovieService(db).delete_movie(id)
    """ for item in movies:
        if item["id"] == id:
            movies.remove(item) """
    return JSONResponse(status_code=200, content={"message": "Se eliminó la película"})
