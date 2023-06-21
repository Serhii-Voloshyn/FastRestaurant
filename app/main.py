import models
from routes import users, employee, menu, menu_item, restaurant, vote

from fastapi import FastAPI
from database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router, tags=['Users'], prefix='/api/routes/users')
app.include_router(employee.router, tags=['Employee'], prefix='/api/routes/employee')
app.include_router(menu.router, tags=['Menu'], prefix='/api/routes/menu')
app.include_router(menu_item.router, tags=['Menu_item'], prefix='/api/routes/menu_item')
app.include_router(restaurant.router, tags=['Restaurant'], prefix='/api/routes/restaurant')
app.include_router(vote.router, tags=['Vote'], prefix='/api/routes/vote')


@app.get("/api/healthchecker")
async def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}
