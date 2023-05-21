from fastapi import FastAPI, Depends
from routers import DataCamera
from config.db import engine, Base


app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(DataCamera.router)



