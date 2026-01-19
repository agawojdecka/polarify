from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.core.config import settings
from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import Base, get_db
from app.domain.user import User as UserDomain
from app.main import app
from app.models.user import User as UserModel

test_database_url = settings.TEST_DATABASE_URL
if test_database_url is None:
    raise ValueError("TEST_DATABASE_URL not found.")


engine = create_engine(str(test_database_url))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    with client as test_client:
        yield test_client

    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def test_auth_client(db_session):
    """
    Create a test client that uses override_get_db fixture to return a session
    and override_get_current_user fixture to authenticate against the database.
    """
    # for "1234" password
    password_hash = (
        "$5$rounds=535000$abhPWTGj/BQ8B7Cx$OBYnr8N0ZR/j0sFHB40VoEaftoLPe7PzrJTfH8Uhhu3"
    )
    fake_db_user = UserModel(
        username="testuser", email="test@example.com", password_hash=password_hash
    )
    db_session.add(fake_db_user)
    db_session.commit()
    db_session.refresh(fake_db_user)

    fake_user = UserDomain(
        id=1, username="testuser", email="test@example.com", created_at=datetime.now()
    )

    def override_get_current_user():
        return fake_user

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)

    with client as test_auth_client:
        yield test_auth_client

    app.dependency_overrides = {}
