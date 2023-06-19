from database import Base
from sqlalchemy import (
    Column, String, Boolean, Integer,
    ForeignKey, Float, Date
)
import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=False)


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey(Restaurant.id))
    day = Column(Date, default=datetime.datetime.utcnow)


class MenuItem(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey(Menu.id))
    name = Column(String, nullable=False)
    price = Column(Float(2), nullable=False)


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(Employee.id))
    menu_id = Column(Integer, ForeignKey(Menu.id))
    score = Column(Integer)
