import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
# Sirve para manipular todas las tablas de la base de datos
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "../database.sqlite"
# Se lee el directorio actual
base_dir = os.path.dirname(os.path.realpath(__file__))

#Url de la base de datos
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Representa el motor de la base de datos
# echo=True es para que muestre en consola lo que se está realizando al crear la base de datos
engine = create_engine(database_url, echo=True)

# Sesión para conectarme a base de datos
Session = sessionmaker(bind=engine)

# Instancia
Base = declarative_base()