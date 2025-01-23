import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from app.main import app
from app.database import get_session

# Replace with your PostgreSQL test database URL
DATABASE_URL_TEST = "postgresql://duytien:okbaby@localhost:5432/test_db"

@pytest.fixture(name="session")
def session_fixture():
    """
    Create a database session for testing, and clean up the database schema after tests.
    """
    # Create an engine for the PostgreSQL test database
    engine = create_engine(DATABASE_URL_TEST)
    SQLModel.metadata.create_all(engine)  # Apply database schema

    # Provide a session connected to the test database
    with Session(engine) as session:
        yield session

    # Clean up after the tests by dropping the schema
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Create a TestClient for the FastAPI app with an overridden session.
    """
    # Override the dependency for session
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override  # Set override

    client = TestClient(app)  # Initialize TestClient with the FastAPI app
    yield client  # Yield client for test use

    app.dependency_overrides.clear()  # Clear overrides after test





