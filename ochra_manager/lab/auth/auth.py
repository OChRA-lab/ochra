from typing import Optional
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
import os

import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import Session

import hashlib
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from datetime import datetime

Base = declarative_base()

# Get the DATABASE_URL from environment variables
AUTH_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")  # Default to SQLite if not set


engine = create_engine(AUTH_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_user_db():
    print("Create all tables in the database.")
    inspector = inspect(engine)
    if not inspector.has_table('your_table_name'):  # You should specify a table name here
        Base.metadata.create_all(bind=engine)
    else:
        print("Tables already exist, skipping creation.")

def get_db():
    """Dependency for accessing the database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


class SessionToken(Base):
    __tablename__ = "session_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.username"), nullable=False)
    token = Column(String, unique=True, index=True)
    created_at = Column(String, default=datetime.utcnow().isoformat)

    user = relationship("User")

    @classmethod
    def get_user_from_session(cls, token: str, db: Session) -> Optional[User]:
        session = db.query(SessionToken).filter(SessionToken.token == token).first()
        if session:
            return session.user
        return None

    @classmethod
    def create_session_token(cls, user_id: int, db: Session):
        token = hashlib.sha256(f"{user_id}-{datetime.utcnow().isoformat()}".encode()).hexdigest()
        session_token = cls(user_id=user_id, token=token)
        db.add(session_token)
        db.commit()
        return token

    @classmethod
    def get_session(cls, db: Session, token: str):
        return db.query(cls).filter(cls.token == token).first()
