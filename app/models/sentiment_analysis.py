from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.api.dependencies.database import Base


class SentimentAnalysisResult(Base):
    __tablename__ = "sentiment_analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    created_at = Column(DateTime, default=func.now())
    opinions_count = Column(Integer, nullable=False)
    positive_count = Column(Integer, nullable=False)
    neutral_count = Column(Integer, nullable=False)
    negative_count = Column(Integer, nullable=False)
    avg_sentiment = Column(Float, nullable=False)

    project = relationship(  # type: ignore
        "Project", back_populates="sentiment_analysis_results"
    )
    user = relationship(  # type: ignore
        "User", back_populates="sentiment_analysis_results"
    )
