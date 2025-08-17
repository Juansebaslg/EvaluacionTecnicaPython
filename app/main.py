# app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

# --- 1. Importaciones para Rate Limiting ---
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware # <-- ESTA ES LA PIEZA QUE FALTABA

from app.core.errors import app_exception_handler, validation_exception_handler, http_exception_handler, AppException
from app.db.base import init_db
from app.api.routes.health import router as health_router
from app.api.routes.messages import router as messages_router

# --- 2. Configuración del Limitador ---
# Limita a todas las rutas a 20 peticiones por minuto por cada IP
limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])


def create_app() -> FastAPI:
    app = FastAPI(title="Chat Messages API", version="1.0.0")

    # --- 3. APLICAR el limitador a la app usando un Middleware ---
    # Esto intercepta cada petición y aplica el límite
    app.add_middleware(SlowAPIMiddleware)
    app.state.limiter = limiter

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Manejadores de errores personalizados
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)

    # Routers
    app.include_router(health_router)
    app.include_router(messages_router)

    # Initialize DB on startup
    @app.on_event("startup")
    def on_startup():
        init_db()

    return app

app = create_app()