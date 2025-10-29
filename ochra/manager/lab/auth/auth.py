from typing import Optional
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
import os

import hashlib
from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Get the DATABASE_URL from environment variables
AUTH_DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./auth.db"
)  # Default to SQLite if not set


engine = create_engine(AUTH_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_user_db() -> None:
    """
    Initialize the user database. Creates tables if they do not exist.
    """
    inspector = inspect(engine)
    if not inspector.has_table(
        "your_table_name"
    ):  # You should specify a table name here
        Base.metadata.create_all(bind=engine)
    else:
        # Tables already exist, skipping creation.
        pass


def get_db() -> Session:
    """
    Yields a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    """
    User model for authentication.

    Attributes:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The hashed password of the user.
    """

    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

    @classmethod
    def fetch_user(cls, db: Session, username: str):
        """
        Fetch a user by username.

        Args:
            db (Session): The database session.
            username (str): The username of the user to fetch.

        Returns:
            Optional[User]: The user object if found, None otherwise.
        """
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def authenticate_user(
        cls, username: str, password: str, db: Session
    ) -> Optional["User"]:
        """
        Authenticate a user by username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            db (Session): The database session.

        Returns:
            Optional[User]: The authenticated user object if successful, None otherwise.
        """
        user = cls.fetch_user(db, username)
        if user and cls.verify_password(password, str(user.password)):
            return user
        return None


class SessionToken(Base):
    """
    SessionToken model for managing user sessions.

    Attributes:
        id (int): The primary key of the session token.
        user_id (str): The ID of the user associated with the session.
        token (str): The unique session token.
        created_at (str): The timestamp when the session was created.
    """

    __tablename__ = "session_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.username"), nullable=False)
    token = Column(String, unique=True, index=True)
    created_at = Column(String, default=datetime.utcnow().isoformat)

    user = relationship("User")

    @classmethod
    def get_user_from_session(cls, token: str, db: Session) -> Optional[User]:
        """
        Get the user associated with a session token.

        Args:
            token (str): The session token.
            db (Session): The database session.

        Returns:
            Optional[User]: The user object if found, None otherwise.
        """
        session = db.query(SessionToken).filter(SessionToken.token == token).first()
        if session:
            return session.user
        return None

    @classmethod
    def create_session_token(cls, user_id: int, db: Session) -> str:
        """
        Create a new session token for a user.

        Args:
            user_id (int): The ID of the user.
            db (Session): The database session.

        Returns:
            str: The generated session token.
        """
        token = hashlib.sha256(
            f"{user_id}-{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()
        session_token = cls(user_id=user_id, token=token)
        db.add(session_token)
        db.commit()
        return token

    @classmethod
    def get_session(cls, db: Session, token: str) -> Optional["SessionToken"]:
        """
        Retrieve a session by its token.
        
        Args:
            db (Session): The database session.
            token (str): The session token.
        
        Returns:
            Optional[SessionToken]: The session object if found, None otherwise.
        """
        return db.query(cls).filter(cls.token == token).first()
