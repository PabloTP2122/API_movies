from jwt import encode, decode

# Función para crear tokens
def create_token(data: dict):
    token: str = encode(payload=data, key="key_secret", algorithm="HS256")
    return token


# Función para validar tokens
def validate_token(token: str) -> str:
     data: dict = decode(token, key="key_secret", algorithms=['HS256'])
     return data