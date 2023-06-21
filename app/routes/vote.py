from fastapi import Depends, status, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import exc
from sqlalchemy.sql import func
from typing import Annotated
from utils import get_current_active_user

import models
import schemas
from database import get_db


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, name="vote_create")
async def create_vote(
    payload: schemas.Vote,
    response: Response,
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):

    vote_dict = payload.dict()
    menu_id = vote_dict["menu_id"]
    menu = db.query(models.Menu).filter_by(id=menu_id).all()

    if not menu:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Menu doesn't exist", "vote": vote_dict}

    employee_id = vote_dict["employee_id"]
    employee = db.query(models.Employee).filter_by(id=employee_id).all()

    if not employee:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Employee doesn't exist", "vote": vote_dict}

    employee_votes = db.query(models.Vote).filter_by(
        employee_id=employee_id, menu_id=menu_id
        ).all()

    if employee_votes:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Employee already voted", "vote": vote_dict}

    new_vote = models.Vote(**vote_dict)
    db.add(new_vote)

    try:
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid data", "vote": vote_dict}

    return {"message": "Successfully created", "vote": vote_dict}


@router.get(
    path="/{menu_id}",
    status_code=status.HTTP_201_CREATED,
    name="vote_get_by_menu"
)
async def get_vote_by_menu(
    menu_id: int,
    response: Response,
    db: Session = Depends(get_db)
):

    menu = db.query(models.Menu).filter_by(id=menu_id).all()

    if not menu:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Menu doesn't exist"}

    votes = db.query(models.Vote).filter_by(menu_id=menu_id).all()
    avg = db.query(
        func.avg(models.Vote.score)
    ).filter_by(menu_id=menu_id).one()

    return {"message": "Successfully retreived", "vote": votes, "avg": avg[0]}
