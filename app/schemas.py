from pydantic import BaseModel

# from enum import Enum


# ------- User status Enum ---------
class Status:
    @classmethod
    def available(cls) -> str:
        return "Available"

    @classmethod
    def in_use(cls) -> str:
        return "In-use"


# --- Data Format for response ----
class ResponseData(BaseModel):
    user_id: int
    session_id: int
    balance: int
    status: str


# ---- Data Format for "inc" request ----
class IncRequestData(BaseModel):
    user_id: int
    password: str
    amount: int


# ---- Data Format for "reset" request ----
class ResetRequestData(BaseModel):
    user_id: int
    password: str


# ---- Data Format for "sync" request ----
class SyncRequestData(BaseModel):
    user_id: int
    session_id: int


# ---- Data Formtat for "verify_password" request ----
class VerifyRequestData(BaseModel):
    password: str
