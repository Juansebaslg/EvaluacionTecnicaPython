# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import create_app
from app.api.deps import get_db
from app.core.config import settings
from app.db.base import Base
import app.db.models

# --- Configuración de la Base de Datos de Pruebas ---
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Crea las tablas una vez al inicio de la sesión de pruebas."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def clear_tables():
    """Limpia todas las tablas después de cada test."""
    yield
    with engine.connect() as connection:
        transaction = connection.begin()
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(text(f"DELETE FROM {table.name};"))
        transaction.commit()


@pytest.fixture(scope="module")
def client():
    """Crea un cliente de prueba que usa la BD en memoria y añade la API Key."""
    app = create_app()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        api_key = getattr(settings, 'API_KEY', 'test-key')
        test_client.headers.update({"X-API-Key": api_key})
        yield test_client
