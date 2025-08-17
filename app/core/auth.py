from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

# Nombre del header que usaremos en la API
API_KEY_NAME = "X-API-Key"
API_KEY = "supersecretkey"  # Reemplaza con tu clave real

# Configuramos FastAPI para que busque este header
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> bool:
    """
    Verifica que la API key enviada en el header sea válida.
    """
    if api_key == API_KEY:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

