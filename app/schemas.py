from datetime import date
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str | None = None


class Restaurant(BaseModel):
    name: str


class Menu(BaseModel):
    restaurant_id: int
    day: date


class Employee(BaseModel):
    full_name: str
    email: EmailStr


class MenuItem(BaseModel):
    menu_id: int
    name: str
    price: float


class Vote(BaseModel):
    menu_id: int
    employee_id: int
    score: int
