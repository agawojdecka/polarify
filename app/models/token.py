from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.api.dependencies.database import Base


class AuthToken(Base):
    __tablename__ = "auth_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False, unique=True
    )
    token = Column(String, index=True, nullable=False)

    user = relationship("User", back_populates="token")  # type: ignore
