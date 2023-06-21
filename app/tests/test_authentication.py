import pytest

from .fixtures import client, tear_down_db, create_user, override_get_db
from main import app


# Username is needed for the create_user fixture,
# login_username -- data for a login request
@pytest.mark.parametrize(
   "username, login_username, password, status_code", [
       ("", "", "", 422),
       ("username", "username", "1234", 400),
       ("username", "username2", "12341235", 400),
       ("username", "username", "12341235", 200),
   ]
)
def test_create_user(
    login_username, tear_down_db, username,
    password, status_code, create_user
):
    login = {
        "username": login_username,
        "password": create_user["password"]
    }

    response = client.post(
        app.url_path_for("login"),
        data=login,
    )
    data = response.json()

    assert response.status_code == status_code

    if status_code == 200:
        assert "access_token" in data.keys()
        assert data["access_token"] is not None

    if status_code == 400:
        assert "access_token" not in data.keys()
