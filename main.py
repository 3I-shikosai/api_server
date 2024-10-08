from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from enum import Enum
from starlette.middleware.cors import CORSMiddleware

# ------- CONSTANTS --------
MAX_USERS = 10
INITIAL_BALANCE = 100
PASSWORD = "hello"

app = FastAPI()


# ------- allow CORS access --------
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
        )


# ------- User status Enum ---------
class Status(str, Enum):
    available = "Available"
    in_use = "In-use"


# ------- Response Data format ---------
class ResponseData(BaseModel):
    user_id: int = None
    session_id: int = None
    balance: int = None
    status: Status = None


# ------- format for update data from user --------
class UpdateData(BaseModel):
    password: str = None
    user_id: int = None
    diff: int = None


# ------- User Class (holds user's status) -------
class Users():
    __user_id: int = None
    __balance: int = None
    __session_id: int = None
    __status: Status = None

    def __init__(self, user_id):
        self.__user_id = user_id
        self.__balance = INITIAL_BALANCE
        self.__status = Status.available
        self.__session_id = 5

    def user_id(self):
        return self.__user_id

    def login(self):
        self.__status = Status.in_use

    def session_id(self):
        return self.__session_id

    def status(self):
        return self.__status

    def balance(self):
        return self.__balance

    def inc(self, diff):
        self.__balance += diff

    def reset(self):
        self.__session_id = self.__session_id + 2 + self.__session_id % 3
        self.balance = INITIAL_BALANCE
        self.__status = Status.available

    def response(self):
        ret = ResponseData()
        ret.user_id = self.__user_id
        ret.session_id = self.__session_id
        ret.balance = self.__balance
        ret.status = self.__status
        return ret


# ---- INIT USERS ----
global_users = [Users(i) for i in range(0, MAX_USERS)]


def get_users():
    global global_users
    return global_users
# --------------------


# ----------- Return user's balance ------------
@app.get("/api/balance/{user_id}")
async def status(user_id: int, users: Users = Depends(get_users)):
    return {"balance": users[user_id].balance}


# ----------- Increament user's balance -------
@app.put("/api/inc")
async def inc(data: UpdateData, users: Users = Depends(get_users)):

    # Increase of Decrease user's balance
    if data.password == PASSWORD:
        users[data.user_id].inc(data.diff)

    return users[data.user_id].response()


# ----------- Reset user's data for next customer -------
@app.put("/api/reset")
async def reset(data: UpdateData, users: Users = Depends(get_users)):

    # Reset user's data
    if data.password == PASSWORD:
        users[data.user_id].reset()
        print("\n [reset] notice\n", users[data.user_id].response(), "\n")

        return users[data.user_id].response()
    else:
        print("\n [reset] error -> password incorrect!!!\n")


# ----------- Return Session ID & change status to in-use -----------
@app.get("/api/user/login/{user_id}")
async def login(user_id: int, users: Users = Depends(get_users)):
    if users[user_id].status() == Status.in_use:

        print("\n[login] error -> status = in_use")

        raise HTTPException(status_code=400, detail="このIDは現在使用中です")

    else:
        users[user_id].login()

        print("\n[login] notice -> login successed", users[user_id].response())
        print("\n")

        return users[user_id].response()


# ----------- Check if the user's data is correct ----------
@app.post("/api/user/sync")
async def sync_data(data: ResponseData, users: Users = Depends(get_users)):
    user = users[data.user_id]
    if data.session_id != user.session_id():

        print("\n[sync] error -> session_id incorrect\n")
        print("server: ", user.response())
        print("\nclient: ", data)
        print("\n")

        raise HTTPException(status_code=400, detail="セッションIDが期限切れです")
    return user.response()
