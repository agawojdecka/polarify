from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.api.dependencies.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    token = relationship(  # type: ignore
        "AuthToken",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    projects = relationship(  # type: ignore
        "Project", back_populates="user", cascade="all, delete-orphan"
    )
