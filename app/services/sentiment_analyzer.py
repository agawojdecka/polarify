import csv
import io
import json
from dataclasses import dataclass
from statistics import mean, median, pstdev

from fastapi import HTTPException
from google import genai
from google.genai import types
from starlette.datastructures import UploadFile

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
    client = genai.Client()

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
