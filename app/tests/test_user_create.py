import pytest

import models
from .fixtures import app, client, tear_down_db, override_get_db


@pytest.mark.parametrize(
   "username, email, full_name, password, status_code, count", [
       ("", "", "", "", 422, 0),
       ("", "ser@gmail.com", "ser", "12341234", 422, 0),
       ("username", "", "ser", "12341234", 422, 0),
       ("username1", "ser@gmail.com", "", "12341234", 201, 1),
       ("username", "ser@gmail.com", "ser", "", 422, 0),
       ("username", "ser", "ser", "12341234", 422, 0),
       ("username", "ser", "ser", "1234", 422, 0),
       ("username2", "ser@gmail.com", "ser", "12341234", 201, 1),
   ]
)
def test_create_user(
    username, email, full_name, password,
    status_code, count, tear_down_db
):
    test_user = {
        "username": username,
        "email": email,
        "full_name": full_name,
        "password": password
    }
    response = client.post(
        app.url_path_for("user_create"),
        json=test_user,
    )

    db = next(override_get_db())
    assert response.status_code == status_code

    assert db.query(models.User).count() == count
