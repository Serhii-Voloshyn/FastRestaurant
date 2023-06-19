from fastapi import Depends, status, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import Annotated
from utils import get_current_active_user

import models
import schemas
from database import get_db


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, name="employee_create")
async def create_employee(
    payload: schemas.Employee,
    response: Response,
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):

    employee_dict = payload.dict()

    new_employee = models.Employee(**employee_dict)
    db.add(new_employee)

    try:
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid data", "employee": employee_dict}

    return {"message": "Successfully created", "employee": employee_dict}
