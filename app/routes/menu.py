from fastapi import Depends, status, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import Annotated
from utils import get_current_active_user
import datetime

import models
import schemas
from database import get_db


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, name="menu_create")
async def create_menu(
    payload: schemas.Menu,
    response: Response,
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    menu_dict = payload.dict()
    restaurant_id = menu_dict["restaurant_id"]
    restaurant = db.query(models.Restaurant).filter_by(id=restaurant_id).all()

    if not restaurant:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Restaurant doesn't exist", "menu": menu_dict}

    new_menu = models.Menu(**menu_dict)
    db.add(new_menu)

    try:
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid data", "menu": menu_dict}

    return {"message": "Successfully created", "menu": menu_dict}


@router.get("/all", status_code=status.HTTP_200_OK, name="menu_get_all")
async def get_all(
    db: Session = Depends(get_db)
):
    menus = db.query(models.Menu).all()
    return {
        'message': 'Successfully retreived',
        'results': len(menus), 'menus': menus
    }


@router.get("/{day}", status_code=status.HTTP_200_OK, name="menu_get_by_day")
async def get_by_day(
    day: datetime.date,
    db: Session = Depends(get_db)
):
    menus = db.query(models.Menu).filter_by(day=day).all()

    for menu in menus:
        menu.items = db.query(models.MenuItem).filter_by(menu_id=menu.id).all()

    return {
        'message': 'Successfully retreived',
        'results': len(menus),
        'menus': menus
    }
