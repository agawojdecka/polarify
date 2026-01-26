from datetime import date

from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.models.sentiment_analysis import SentimentAnalysisResult


def create_sentiment_analysis_result(
    db: Session,
    project_id: int,
    user_id: int,
    date_from: date,
    date_to: date,
    opinions_count: int,
    positive_count: int,
    neutral_count: int,
    negative_count: int,
    avg_sentiment: float,
) -> SentimentAnalysisResult:
    db_sentiment_analysis_result = SentimentAnalysisResult(
        project_id=project_id,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
        opinions_count=opinions_count,
        positive_count=positive_count,
        neutral_count=neutral_count,
        negative_count=negative_count,
        avg_sentiment=avg_sentiment,
    )
    db.add(db_sentiment_analysis_result)
    db.commit()
    db.refresh(db_sentiment_analysis_result)

    return db_sentiment_analysis_result


def get_sentiment_analysis_results(
    db: Session,
    project_id: int,
    user_id: int,
    year: int | None = None,
) -> list[SentimentAnalysisResult]:
    query = db.query(SentimentAnalysisResult).filter(
        SentimentAnalysisResult.project_id == project_id,
        SentimentAnalysisResult.user_id == user_id,
    )

    if year:
        query = query.filter(
            (extract("year", SentimentAnalysisResult.date_from) == year)
            | (extract("year", SentimentAnalysisResult.date_to) == year)
        )

    return query.order_by(SentimentAnalysisResult.created_at.desc()).all()
