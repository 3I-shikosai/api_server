from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import services
from .db import database
from . import schemas
from .utils import Password

router = APIRouter()


@router.put("/api/verify_password")
def verify_password(request: schemas.VerifyRequestData):

    if not Password.verify(request.password):
        return {"result": False}

    return {"result": True}


@router.get("/api/balance/{user_id}")
def balance(user_id: int, db: Session = Depends(database.get_db)):
    user = services.User(db)
    response = user.balance(user_id)

    if response is None:
        raise HTTPException(status_code=400, detail="User Not Found")

    return {"balance": response}


@router.put("/api/increase")
def increase_balance(
    request: schemas.IncRequestData, db: Session = Depends(database.get_db)
):
    user = services.User(db)

    if not (Password.verify(request.password)):
        raise HTTPException(status_code=400, detail="Incorrect Password")

    response = user.increase_balance(request.user_id, request.amount)

    if response is None:
        raise HTTPException(status_code=400, detail="User Not Fount")

    return response


@router.put("/api/reset")
def reset(
    request: schemas.ResetRequestData, db: Session = Depends(database.get_db)
):
    user = services.User(db)

    if not (Password.verify(request.password)):
        raise HTTPException(status_code=400, detail="Incorrect Password")

    response = user.reset(request.user_id)

    if response is None:
        raise HTTPException(status_code=400, detail="User Not Fount")

    return response


@router.get("/api/user/login/{user_id}")
def login(user_id: int, db: Session = Depends(database.get_db)):
    user = services.User(db)
    response = user.login(user_id)

    if response is None:
        raise HTTPException(
            status_code=400, detail="The UserID is currently In-Use"
        )

    return response


@router.put("/api/user/sync")
def sync(
    request: schemas.SyncRequestData, db: Session = Depends(database.get_db)
):
    user = services.User(db)
    response = user.response(request.user_id)

    if not (response.session_id == request.session_id):
        raise HTTPException(status_code=400, detail="Invalid SessionID")

    return response
