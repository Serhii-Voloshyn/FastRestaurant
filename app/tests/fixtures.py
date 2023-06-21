from database import get_db, Base
from main import app
import models

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture()
def username():
    return "ser"


@pytest.fixture()
def password():
    return "bananas123"


@pytest.fixture()
def tear_down_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def create_user(tear_down_db, username, password):
    user = {
        "username": username,
        "password": password,
        "full_name": "ser",
        "email": "ser@gmail.com"
    }

    client.post(app.url_path_for("user_create"), json=user)

    return user


@pytest.fixture()
def create_restaurant(tear_down_db):
    restaurant = {
        "name": "bananas"
    }
    restaurant = models.Restaurant(**restaurant)

    db = next(override_get_db())
    db.add(restaurant)
    db.commit()

    return restaurant


@pytest.fixture()
def login_header(tear_down_db, create_user):
    login = {
        "username": create_user["username"],
        "password": create_user["password"]
    }
    access_token = client.post(
        app.url_path_for("login"),
        data=login,
    ).json()["access_token"]

    return {"Authorization": f"Bearer {access_token}"}
