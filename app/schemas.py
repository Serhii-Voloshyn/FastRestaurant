from datetime import date
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    full_name: str | None
    password: str = Field(min_length=8)


class Token(BaseModel):
    access_token: str | None
    token_type: str | None
    username: str | None = None


class Restaurant(BaseModel):
    name: str = Field(min_length=1)


class Menu(BaseModel):
    restaurant_id: int
    day: date


class Employee(BaseModel):
    full_name: str = Field(min_length=1)
    email: EmailStr


class MenuItem(BaseModel):
    menu_id: int
    name: str
    price: float


class Vote(BaseModel):
    menu_id: int
    employee_id: int
    score: int
