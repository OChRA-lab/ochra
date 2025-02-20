import hashlib
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from ..main import Base
from datetime import datetime


class SessionToken(Base):
    __tablename__ = "session_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.username"), nullable=False)
    token = Column(String, unique=True, index=True)
    created_at = Column(String, default=datetime.utcnow().isoformat)

    user = relationship("User")

    @classmethod
    def get_user_from_session(cls, token: str, db: Session):
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
