from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from random import randint

from . import schemas
from .config import Constants
from . import routers
from .db import database, models

app = FastAPI()


# ------- allow CORS access --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------- create DB table ----------
database.Base.metadata.create_all(bind=database.engine)


# ------- create users on DB ----------
def create_users(db: Session):
    if db.query(models.User).count() == 0:
        for i in range(Constants.TOTAL_USERS()):
            new_user = models.User(
                user_id=i,
                session_id=randint(100, 1000000),
                balance=Constants.INITIAL_BALANCE(),
                status=schemas.Status.available(),
            )
            db.add(new_user)
        db.commit()


@app.on_event("startup")
def startup_event():
    db = database.SessionLocal()
    create_users(db)
    db.close()


app.include_router(routers.router)
