from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from starlette.middleware.cors import CORSMiddleware

import threading

# for Debug coloring
from colorama import Fore, Style


# ------- for Debug -------
def note(str: str):
    print(Fore.YELLOW)
    print(f'\n------ [[ {str} ]] ---------------------------')
    print(Style.RESET_ALL)


def note_():
    print(Fore.YELLOW)
    print("\n---")
    print(Style.RESET_ALL)


def warn(str: str):
    print(Fore.RED)
    print(f'\n------ [[ {str} ]] ---------------------------')
    print(Style.RESET_ALL)


def warn_():
    print(Fore.RED)
    print("\n---")
    print(Style.RESET_ALL)


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

    def __init__(self, user_id):
        self.__user_id = user_id
        self.__balance = INITIAL_BALANCE
        self.__status = Status.available
        self.__session_id = 5

    @property
    def user_id(self):
        return self.__user_id

    def login(self):
        self.__status = Status.in_use

    @property
    def get_session_id(self):
        return self.__session_id

    @property
    def status(self):
        return self.__status

    @property
    def balance(self):
        return self.__balance

    def inc(self, diff):
        self.__balance += diff

    def reset(self):
        self.__session_id = self.__session_id + 2 + self.__session_id % 3
        self.balance = INITIAL_BALANCE
        self.__status = Status.available

    def response(self):
        return ResponseData(
                user_id=self.__user_id,
                session_id=self.__session_id,
                balance=self.__balance,
                status=self.__status
        )


# ---- INIT USERS ----
global_users = [Users(i) for i in range(0, MAX_USERS)]


lock = threading.Lock()
# --------------------


# ----------- Return user's balance ------------
@app.get("/api/balance/{user_id}")
async def status(user_id: int):
    global global_users

    note("Balance")
    print("User(server):", global_users[user_id].response())
    note_()

    return {"balance": (global_users[user_id]).balance}


# ----------- Increament user's balance -------
@app.put("/api/inc")
async def inc(data: UpdateData):

    global global_users

    note("Inc Call")
    print("UpdateData(client):", data)
    print("User(server):", global_users[data.user_id].response())
    note_()

    if data.password == PASSWORD:
        with lock:
            global_users[data.user_id].inc(data.diff)

    else:

        warn("Increase")
        print("管理者パスワードが間違っています")
        warn_()

        raise HTTPException(status_code=400, detail="管理者パスワードが間違っています")

    note("Inc Fin!")
    print("User:", global_users[data.user_id].response())
    note_()

    return global_users[data.user_id].response()


# ----------- Reset user's data for next customer -------
@app.put("/api/reset")
async def reset(data: UpdateData):
    global global_users

    note("Reset Call")
    print("UpdateData(client):", data)
    print("User(server):", global_users[data.user_id].response())
    note_()
    note_()

    if data.password == PASSWORD:
        with lock:
            global_users[data.user_id].reset()

    else:
        warn("Increase")
        print("管理者パスワードが間違っています")
        warn_()

        raise HTTPException(status_code=400, detail="管理者パスワードが間違っています")

    note("Reset Fin!")
    print("User:", global_users[data.user_id].response())
    note_()

    return global_users[data.user_id].response()


# ----------- Return Session ID & change status to in-use -----------
@app.get("/api/user/login/{user_id}")
async def login(user_id: int):
    global global_users

    note("Login Call")
    print("user_id:", user_id)
    note_()

    if global_users[user_id].status == Status.in_use:

        warn("Login")
        print("ID使用中 status==Status.in_use")
        warn_()

        raise HTTPException(status_code=400, detail="このIDは現在使用中です")

    else:
        with lock:
            global_users[user_id].login()

    note("Login Fin!")
    print("User:", global_users[user_id].response())
    note_()

    return global_users[user_id].response()


# ----------- Check if the user's data is correct ----------
@app.post("/api/user/sync")
async def sync_data(data: ResponseData):
    global global_users
    
    note("SYNC Call")
    print("ResponseData(client):", data)
    print("User(server):", global_users[data.user_id].response())
    note_()

    if data.session_id != global_users[data.user_id].get_session_id:

        warn("SYNC")
        print("セッションID期限切れ")
        warn_()

        raise HTTPException(status_code=400, detail="セッションIDが期限切れです")

    note("SYNC Fin!")
    print("User:", global_users[data.user_id].response())
    note_()

    return global_users[data.user_id].response()
