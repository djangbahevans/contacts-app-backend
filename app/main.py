import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import database, models
from .routers import auth, contact, user

logging.basicConfig(filename="app.log")
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=[],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

app.include_router(auth.router)
app.include_router(contact.router)
app.include_router(user.router)


@app.get('/')
def root():
    return "Welcome to my contacts API"
