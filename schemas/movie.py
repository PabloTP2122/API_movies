# Para crear esquemas
from pydantic import BaseModel, Field
# Ayuda a colocar valores opcionales
from typing import Optional


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
                # El ID es generado por la base de datos
                # "id": 1,
                "title": "Título",
                "overview": "Describe la película",
                "year": 2022,
                "rating": 5.0,
                "category": "categoría"
            }

        }


""" 
# Ejemplo de representación de movies
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
 """
