import schemas
import models
from sqlalchemy.orm import Session
from sqlalchemy import exc

from typing import Annotated
from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status, APIRouter, Response

from database import get_db

from utils import (
    get_current_active_user, get_password_hash, authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
)


router = APIRouter()


@router.post(
    path="/token",
    status_code=status.HTTP_200_OK,
    name="login"
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: Session = Depends(get_db)
):
    try:
        user = await authenticate_user(
            form_data.username,
            form_data.password,
            db,
            response
        )
    except exc.NoResultFound:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Username doesn't exist"}

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = await create_access_token(
        data={"sub": user.username},
        response=response,
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }


@router.get(
    path="/me/",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    name="user_me"
)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    user = current_user
    return schemas.User(**user.__dict__)


@router.post("/", status_code=status.HTTP_201_CREATED, name="user_create")
async def create_user(
    payload: schemas.User,
    response: Response,
    db: Session = Depends(get_db)
):

    user_dict = payload.dict()
    user_dict["password"] = await get_password_hash(user_dict["password"])

    new_user = models.User(**user_dict)
    db.add(new_user)

    try:
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid data", "user": user_dict}

    return {"message": "Successfully created", "user": user_dict}


@router.get("/", status_code=status.HTTP_200_OK)
async def read_users_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {
        'message': 'Successfully retreived',
        'results': len(users),
        'users': users
    }
