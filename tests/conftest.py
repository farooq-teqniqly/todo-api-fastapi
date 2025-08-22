import pytest
from faker import Faker
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base
from fastapi.testclient import TestClient

@pytest.fixture(scope="function")
def fake():
    f = Faker()
    Faker.seed(206)
    return f

@pytest.fixture(scope="function")
def postgres_container():
    with PostgresContainer("postgres:17.5") as container:
        container.start()
        yield container

@pytest.fixture(scope="function")
def override_db(postgres_container):
    connection_url = postgres_container.get_connection_url()
    connection_url = connection_url.replace("psycopg2", "psycopg")
    engine = create_engine(connection_url)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    Base.metadata.create_all(bind=engine)

    def _get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_test_db

@pytest.fixture
def client(override_db):
    return TestClient(app)
