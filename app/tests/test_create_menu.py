import pytest

import models
from .fixtures import (
    app, client, tear_down_db, override_get_db, create_restaurant,
    login_header, create_user, username, password
)


@pytest.mark.parametrize(
   "restaurant_id, date, status_code, count", [
       ("0", "2023-06-19", 400, 0),
       ("1", "2023-06-19-01", 422, 0),
       ("1", "2023-06-19", 201, 1)
   ]
)
def test_create_restaurant(
    restaurant_id, date, status_code, count,
    tear_down_db, create_restaurant, login_header
):
    menu = {
        "restaurant_id": restaurant_id,
        "day": date,
    }
    response = client.post(
        app.url_path_for("menu_create"),
        json=menu,
        headers=login_header
    )

    db = next(override_get_db())
    assert response.status_code == status_code
    assert db.query(models.Menu).count() == count
