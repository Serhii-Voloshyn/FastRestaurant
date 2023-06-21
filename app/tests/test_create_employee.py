import pytest

import models
from .fixtures import (
    app, client, tear_down_db, override_get_db,
    login_header, create_user, username, password
)


@pytest.mark.parametrize(
   "full_name, email, status_code, count", [
       ("", "", 422, 0),
       ("Ser", "sergmail.com", 422, 0),
       ("Ser", "ser@gmail.com", 201, 1),
   ]
)
def test_create_restaurant(
    full_name, email, status_code,
    count, tear_down_db, login_header
):
    employee = {
        "full_name": full_name,
        "email": email
    }
    response = client.post(
        app.url_path_for("employee_create"),
        json=employee,
        headers=login_header
    )

    db = next(override_get_db())
    assert response.status_code == status_code
    assert db.query(models.Employee).count() == count
