import csv
import io
import json
from dataclasses import dataclass
from datetime import date, datetime
from statistics import StatisticsError, mean, median, pstdev

from fastapi import HTTPException
from google import genai
from google.genai import types
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile

from app.api.core.config import settings
from app.repository.sentiment_analysis import create_sentiment_analysis_result
from app.utils.prompts import PromptTypeE, get_prompt


@dataclass
class Opinion:
    id: str
    content: str


@dataclass
class OpinionsSentiment:
    id: str
    sentiment: float


@dataclass
class OpinionsSentimentAverage:
    value: float


@dataclass
class OpinionsSentimentStatisticalMeasures:
    min: float
    max: float
    mean: float
    median: float
    std: float


def get_sentiment_values(
    opinions_list: list[Opinion],
) -> list[OpinionsSentiment]:
    opinions_str = opinions_list_to_str(opinions_list)
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=get_prompt(PromptTypeE.CONTENT) + opinions_str,
            config=types.GenerateContentConfig(
                system_instruction=get_prompt(PromptTypeE.SYSTEM_INSTRUCTIONS),
                response_mime_type="application/json",
            ),
        )

        if response.text is None:
            raise HTTPException(status_code=400, detail="Failed to get response.")
        else:
            data = json.loads(response.text)
            opinions_sentiment_values = [
                OpinionsSentiment(id=k, sentiment=v) for k, v in data.items()
            ]
            return opinions_sentiment_values

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to generate sentiment {e}."
        )


def get_sentiment_average_value(
    opinions_sentiment: list[OpinionsSentiment],
) -> OpinionsSentimentAverage:
    values = [opinion.sentiment for opinion in opinions_sentiment]
    average_sentiment = round(mean(values), 2)
    return OpinionsSentimentAverage(value=average_sentiment)


def opinions_list_to_str(opinions_list: list[Opinion]) -> str:
    opinions_str = ", ".join(
        f"{opinion.id}: {opinion.content}" for opinion in opinions_list
    )
    return opinions_str


async def opinions_csv_to_list(file: UploadFile) -> list[Opinion]:
    content = await file.read()
    text = content.decode("utf-8")

    reader = csv.reader(io.StringIO(text))

    opinions_list = [Opinion(id=row[0], content=row[1]) for row in reader if row]

    return opinions_list


def calculate_statistical_measures(
    opinions_sentiment: list[OpinionsSentiment],
) -> OpinionsSentimentStatisticalMeasures:
    values = [opinion.sentiment for opinion in opinions_sentiment]

    return OpinionsSentimentStatisticalMeasures(
        min=min(values),
        max=max(values),
        mean=round(mean(values), 2),
        median=median(values),
        std=round(pstdev(values), 2),
    )


@dataclass
class SentimentAnalysisResult:
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


def analyze_sentiment(
    db: Session,
    project_id: int,
    user_id: int,
    date_from: date,
    date_to: date,
    opinions_list: list[Opinion],
) -> SentimentAnalysisResult:

    opinions_sentiment_values = get_sentiment_values(opinions_list)
    opinions_count = len(opinions_sentiment_values)
    positive_count = sum(1 for o in opinions_sentiment_values if o.sentiment > 0.05)

    negative_count = sum(1 for o in opinions_sentiment_values if o.sentiment < -0.05)

    neutral_count = sum(
        1 for o in opinions_sentiment_values if -0.05 <= o.sentiment <= 0.05
    )
    try:
        avg_sentiment = round(mean(o.sentiment for o in opinions_sentiment_values), 2)
    except StatisticsError:
        avg_sentiment = 0.0

    sentiment_analysis_result_repo = create_sentiment_analysis_result(
        db,
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

    sentiment_analysis_result = SentimentAnalysisResult(
        project_id=project_id,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to,
        opinions_count=opinions_count,
        positive_count=positive_count,
        neutral_count=neutral_count,
        negative_count=negative_count,
        avg_sentiment=avg_sentiment,
        created_at=sentiment_analysis_result_repo.created_at,
    )
    return sentiment_analysis_result
