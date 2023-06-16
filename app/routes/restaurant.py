from fastapi import Depends, status, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import Annotated
from utils import get_current_active_user

import models, schemas
from database import get_db


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, name="restaurant_create")
async def create_restaurant(
    payload: schemas.Restaurant,
    response: Response,
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):

    restaurant_dict = payload.dict()

    new_restaurant = models.Restaurant(**restaurant_dict)
    db.add(new_restaurant)

    try:
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid data", "restaurant": restaurant_dict}

    return {"message": "Successfully created", "restaurant": restaurant_dict}
