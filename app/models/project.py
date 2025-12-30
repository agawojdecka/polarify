from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.api.dependencies.database import Base


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="projects")  # type: ignore
    sentiment_analysis_results = relationship(  # type: ignore
        "SentimentAnalysisResult", back_populates="project"
    )
