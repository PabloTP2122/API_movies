from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
# Para crear esquemas
from pydantic import BaseModel, Field
# Ayuda a colocar valores opcionales
from typing import Optional, List
# Base de datos
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

# Manejo de JWT
from middlewares.jwt_bearer import JWTBarer

movie_router = APIRouter()


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


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBarer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# Parametros de la ruta
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
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
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    # return [movie for movie in movies if movie['category'] == category]


# Método POST para crear
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    # Primero hay que crear sesión para conectarse a la base de datos
    db = Session()
    # creada una película
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    # movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha reguistrado correctamente la película"})

# Método PUT para modificar


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": f"No se encontró la película con id:  {id}"})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category

    db.commit()
    """ for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category """
    return JSONResponse(status_code=200, content={"message": f"Se modificó correctamente la película con id:  {id}"})


# Método DELETE
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": f"No se encontró la película con id:  {id}"})
    db.delete(result)
    db.commit()
    """ for item in movies:
        if item["id"] == id:
            movies.remove(item) """
    return JSONResponse(status_code=200, content={"message": "Se eliminó la película"})
