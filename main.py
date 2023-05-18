from fastapi import FastAPI, Depends
from routers import DataCamera, authjwt
from config.db import engine, Base
from models.users import UsersModel



app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(DataCamera.router)
# app.include_router(auth.router)
app.include_router(authjwt.router)

