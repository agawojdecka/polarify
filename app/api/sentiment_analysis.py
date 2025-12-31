from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.domain.user import User as UserDomain
from app.repository import project as project_repo
from app.repository import sentiment_analysis as sentiment_repo
from app.services.sentiment_analysis import (
    Opinion,
    analyze_sentiment,
    opinions_csv_to_list,
)

router = APIRouter()


class OpinionsToAnalyzeRequest(BaseModel):
    id: str
    content: str


class SentimentAnalysisResponse(BaseModel):
    project_id: int
    user_id: int
    date_from: date
    date_to: date
    opinions_count: int
    positive_count: int
    neutral_count: int
    negative_count: int
    avg_sentiment: float
    created_at: datetime


@router.post("/sentiment-analysis-raw")
async def sentiment_analysis_raw(
    project_id: int,
    date_from: date,
    date_to: date,
    opinions_to_analyze: list[OpinionsToAnalyzeRequest],
    db: Session = Depends(get_db),
    current_user: UserDomain = Depends(get_current_user),
) -> SentimentAnalysisResponse:
    opinions_list = [
        Opinion(id=opinion.id, content=opinion.content)
        for opinion in opinions_to_analyze
    ]

    sentiment_analysis_results = analyze_sentiment(
        db,
        project_id=project_id,
        user_id=current_user.id,
        date_from=date_from,
        date_to=date_to,
        opinions_list=opinions_list,
    )

    response = SentimentAnalysisResponse(
        project_id=sentiment_analysis_results.project_id,
        user_id=sentiment_analysis_results.user_id,
        date_from=sentiment_analysis_results.date_from,
        date_to=sentiment_analysis_results.date_to,
        opinions_count=sentiment_analysis_results.opinions_count,
        positive_count=sentiment_analysis_results.positive_count,
        neutral_count=sentiment_analysis_results.neutral_count,
        negative_count=sentiment_analysis_results.negative_count,
        avg_sentiment=sentiment_analysis_results.avg_sentiment,
        created_at=sentiment_analysis_results.created_at,
    )

    return response


@router.post("/sentiment-analysis-csv")
async def sentiment_analysis_csv(
    project_id: int,
    date_from: date,
    date_to: date,
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: UserDomain = Depends(get_current_user),
) -> SentimentAnalysisResponse:

    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a CSV."
        )

    opinions_list = await opinions_csv_to_list(file)

    sentiment_analysis_results = analyze_sentiment(
        db,
        project_id=project_id,
        user_id=current_user.id,
        date_from=date_from,
        date_to=date_to,
        opinions_list=opinions_list,
    )

    response = SentimentAnalysisResponse(
        project_id=sentiment_analysis_results.project_id,
        user_id=sentiment_analysis_results.user_id,
        date_from=sentiment_analysis_results.date_from,
        date_to=sentiment_analysis_results.date_to,
        opinions_count=sentiment_analysis_results.opinions_count,
        positive_count=sentiment_analysis_results.positive_count,
        neutral_count=sentiment_analysis_results.neutral_count,
        negative_count=sentiment_analysis_results.negative_count,
        avg_sentiment=sentiment_analysis_results.avg_sentiment,
        created_at=sentiment_analysis_results.created_at,
    )

    return response


@router.get("/sentiment-analysis_results/{project_id}")
async def get_sentiment_analysis_results(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserDomain = Depends(get_current_user),
) -> list[SentimentAnalysisResponse]:
    project = project_repo.get_project(
        db, project_id=project_id, user_id=current_user.id
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    sentiment_analysis_results = sentiment_repo.get_sentiment_analysis_results(
        db, project_id=project_id, user_id=current_user.id
    )

    response = []
    for sentiment_analysis_result in sentiment_analysis_results:
        response.append(
            SentimentAnalysisResponse(
                project_id=sentiment_analysis_result.project_id,
                user_id=sentiment_analysis_result.user_id,
                date_from=sentiment_analysis_result.date_from,
                date_to=sentiment_analysis_result.date_to,
                opinions_count=sentiment_analysis_result.opinions_count,
                positive_count=sentiment_analysis_result.positive_count,
                neutral_count=sentiment_analysis_result.neutral_count,
                negative_count=sentiment_analysis_result.negative_count,
                avg_sentiment=sentiment_analysis_result.avg_sentiment,
                created_at=sentiment_analysis_result.created_at,
            )
        )
    return response
