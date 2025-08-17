# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.core.errors import app_exception_handler, validation_exception_handler, http_exception_handler, AppException
from app.db.base import init_db
from app.api.routes.health import router as health_router
from app.api.routes.messages import router as messages_router


def create_app() -> FastAPI:
    app = FastAPI(title="Chat Messages API", version="1.0.0")

    # CORS (ajusta orígenes si hace falta)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # <<--- ESTA ES LA PARTE CLAVE QUE FALTABA --- >>
    # Registra los manejadores de errores personalizados
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)

    # Incluir routers
    app.include_router(health_router)
    app.include_router(messages_router)

    # Initialize DB on startup
    @app.on_event("startup")
    def on_startup():
        init_db()

    return app

app = create_app()
