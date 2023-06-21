import pytest

import models
from .fixtures import (
    app, client, tear_down_db, override_get_db,
    create_user, login_header
)


@pytest.mark.parametrize(
   "username, password, name, status_code, count", [
       ("ser", "12341234", "", 422, 0),
       ("ser", "12341234", None, 422, 0),
       ("ser", "12341234", "Why", 201, 1)
   ]
)
def test_create_restaurant(
    username, password, name, status_code, count,
    tear_down_db, create_user, login_header
):
    restaurant = {
        "name": name
    }

    response = client.post(
        app.url_path_for("restaurant_create"),
        json=restaurant,
        headers=login_header
    )

    db = next(override_get_db())
    assert response.status_code == status_code
    assert db.query(models.Restaurant).count() == count
