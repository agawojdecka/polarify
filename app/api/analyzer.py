from dataclasses import asdict

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel

from app.services.sentiment_analysis import (
    Opinion,
    calculate_statistical_measures,
    get_sentiment_average_value,
    get_sentiment_values,
    opinions_csv_to_list,
)

router = APIRouter()


class OpinionsSentimentRequest(BaseModel):
    id: str
    content: str


class OpinionsSentimentResponse(BaseModel):
    id: str
    sentiment: float


class OpinionsSentimentAverageResponse(BaseModel):
    value: float


class OpinionsSentimentStatisticalMeasuresResponse(BaseModel):
    min: float
    max: float
    mean: float
    median: float
    std: float


@router.post("/analyze-sentiment")
async def analyze_sentiment(
    opinions_to_analyze: list[OpinionsSentimentRequest],
) -> list[OpinionsSentimentResponse]:
    opinions_list = [
        Opinion(id=opinion.id, content=opinion.content)
        for opinion in opinions_to_analyze
    ]

    sentiment_values = get_sentiment_values(opinions_list)

    response = [
        OpinionsSentimentResponse(id=item.id, sentiment=item.sentiment)
        for item in sentiment_values
    ]

    return response


@router.post("/analyze-average-sentiment")
async def analyze_average_sentiment(
    opinions_to_analyze: list[OpinionsSentimentRequest],
) -> OpinionsSentimentAverageResponse:
    opinions_list = [
        Opinion(id=opinion.id, content=opinion.content)
        for opinion in opinions_to_analyze
    ]

    sentiment_values = get_sentiment_values(opinions_list)

    average = get_sentiment_average_value(sentiment_values)

    response = OpinionsSentimentAverageResponse(value=average.value)

    return response


@router.post("/analyze-sentiment-csv")
async def analyze_sentiment_csv(file: UploadFile) -> list[OpinionsSentimentResponse]:
    if file.content_type not in ["text/csv", "application/vnd.ms-excel"]:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a CSV."
        )

    opinions_list = await opinions_csv_to_list(file)

    sentiment_values = get_sentiment_values(opinions_list)

    response = [
        OpinionsSentimentResponse(id=item.id, sentiment=item.sentiment)
        for item in sentiment_values
    ]
    return response


@router.post("/analyze-sentiment-statistical-measures")
async def analyze_sentiment_statistical_measures(
    opinions_to_analyze: list[OpinionsSentimentRequest],
) -> OpinionsSentimentStatisticalMeasuresResponse:
    opinions_list = [
        Opinion(id=opinion.id, content=opinion.content)
        for opinion in opinions_to_analyze
    ]

    sentiment_values = get_sentiment_values(opinions_list)
    statistical_measures = calculate_statistical_measures(sentiment_values)

    response = OpinionsSentimentStatisticalMeasuresResponse(
        **asdict(statistical_measures)
    )
    return response
