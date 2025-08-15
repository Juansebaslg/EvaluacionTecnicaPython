import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.db.base import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

@pytest.fixture(scope="session", autouse=True)
def _prepare_db():
    # Use a separate SQLite DB in memory for tests
    test_engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    # Monkeypatch SessionLocal used by the app
    import app.db.base as base_module
    base_module.engine = test_engine
    base_module.SessionLocal = TestingSessionLocal

    yield

    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)

@pytest.fixture
def db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
