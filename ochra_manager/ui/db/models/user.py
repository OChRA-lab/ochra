import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from ..main import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)


    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

    @classmethod
    def fetch_user(cls, db: Session, username: str):
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def authenticate_user(cls, username: str, password: str, db: Session):
        user = cls.fetch_user(db, username)
        if user and cls.verify_password(password, str(user.password)):
            return user
        return None

