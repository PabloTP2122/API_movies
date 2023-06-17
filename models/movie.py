from config.database import Base

from sqlalchemy import Column, Integer, String, Float

# Entidad de la base de datos
class Movie(Base):
    # Nombre de la tabla en base de datos
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)