from fastapi import Depends, status, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import Annotated
from utils import get_current_active_user
import datetime

import models, schemas
from database import get_db


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, name="menu_item_create")
async def create_menu_item(
    payload: schemas.MenuItem,
    response: Response,
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):

    menu_item_dict = payload.dict()
    menu_id = menu_item_dict["menu_id"]
    menu = db.query(models.Menu).filter_by(id=menu_id).all()

    if not menu:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Menu doesn't exist", "menu_item": menu_item_dict}

    new_menu_item = models.MenuItem(**menu_item_dict)
    db.add(new_menu_item)

    try:
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid data", "menu_item": menu_item_dict}

    return {"message": "Successfully created", "menu_item": menu_item_dict}