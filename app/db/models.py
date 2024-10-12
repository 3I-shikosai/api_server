from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    def __str__(self):
        return (
            f"<User(id={self.id}, session_id={self.session_id}, "
            "balance={self.balance}, status={self.status})>"
        )
