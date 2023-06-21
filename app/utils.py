from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, status, Response, HTTPException
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/routes/users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    response: Response,
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise credentials_exception
        token_data = schemas.Token(
            access_token=token,
            token_type="bearer",
            username=username
        )
    except JWTError:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise credentials_exception

    return await get_user(token_data.username, db, response)


async def get_user(username: str, db, response: Response) -> models.User:

    # If none -- raises exc.NoResultFound exception.
    # It is handeled in login route
    return db.query(models.User).filter_by(username=username).one()


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)],
    response: Response
) -> models.User:
    if current_user.disabled:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_user(
    username: str,
    password: str,
    db,
    response: Response
) -> models.User:
    user = await get_user(username, db, response)

    if not await verify_password(password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorect username or password"
        )

    return user


async def create_access_token(
    data: dict,
    response: Response,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
