from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

MAX_USERS = 10

app = FastAPI()


app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
        )


class Users:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__balance = 10

    def user_id(self):
        return self.__user_id

    def balance(self):
        return self.__balance

    def inc(self, diff):
        self.__balance += diff

    def response(self):
        ret = ResponseData()
        ret.user_id = self.__user_id
        ret.balance = self.__balance
        return ret


class UpdateData(BaseModel):
    user_id: int = None
    diff: int = None


class ResponseData(BaseModel):
    user_id: int = None
    balance: int = None


# ---- INIT USERS ----

users = [ Users(i) for i in range(0, MAX_USERS) ]

# --------------------


@app.get("/api/balance/{user_id}")
async def status(user_id: int):
    return users[user_id].response()


@app.put("/api/inc")
async def inc(update_data: UpdateData):
    user = users[update_data.user_id]
    user.inc(update_data.diff) 
    return user.response()
