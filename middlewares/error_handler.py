# Modulo que no viene en FatAPI
import typing
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse


class ErrorHandler(BaseHTTPMiddleware):

    # Método constructor
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    # Método async dispatch para detectar errores en la aplicación.
    # Recibe un parámetro request para acceder a todas las peticiones
    # Se devuelve response o JSONResponse
    async def dispatch(self, request: Request, call_next) -> Response or JSONResponse:
        # Se añade excepción
        try:
            # Si no existe ningún error retorna la siguiente llamada
            return await call_next(request)
        except Exception as e:
            # Si ocurre un error, se retorna el error.
            return JSONResponse(status_code=500, content={'error': str(e)})
