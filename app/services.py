from sqlalchemy.orm import Session
from random import randint

from .db import models
from . import schemas
from .config import Constants


class User:
    def __init__(self, db: Session):
        self.__db = db

    def __get_user(self, user_id: int):
        return (
            self.__db.query(models.User)
            .filter(models.User.user_id == user_id)
            .first()
        )

    def balance(self, user_id: int) -> int:
        user = self.__get_user(user_id)
        if user:
            return user.balance
        return None

    def session_id(self, user_id: int) -> int:
        user = self.__get_user(user_id)
        if user:
            return user.session_id
        return None

    def response(self, user_id: int):
        user = self.__get_user(user_id)
        if user:
            return schemas.ResponseData(
                user_id=user_id,
                session_id=user.session_id,
                balance=user.balance,
                status=user.status,
            )
        return None

    def increase_balance(self, user_id: int, amount: int):
        user = self.__get_user(user_id)
        if user:
            user.balance += amount
            self.__db.commit()
            self.__db.refresh(user)
            return self.response(user_id)
        return None

    def login(self, user_id: int):
        user = self.__get_user(user_id)
        if user:
            user.status = schemas.Status.in_use()
            self.__db.commit()
            self.__db.refresh(user)
            return self.response(user_id)
        return None

    def reset(self, user_id: int):
        user = self.__get_user(user_id)
        if user:
            user.balance = Constants.INITIAL_BALANCE()
            user.session_id = randint(100, 1000000)
            user.status = schemas.Status.available
            self.__db.commit()
            self.__db.refresh(user)
            return self.response(user_id)
        return None
