import hashlib

from .config import Constants


class Password:
    @classmethod
    def encode(cls, raw_str: str) -> str:
        return hashlib.sha256(raw_str.encode()).hexdigest()

    @classmethod
    def verify(cls, raw_password: str) -> bool:
        return cls.encode(raw_password) == Constants.PASSWORD()
