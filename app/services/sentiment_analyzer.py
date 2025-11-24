import csv
import io
import json
from dataclasses import dataclass

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


def get_sentiment_values(
    opinions_list: list[Opinion],
) -> list[OpinionsSentiment]:
    opinions_str = opinions_sentiment_request_list_to_str(opinions_list)
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
    opinions_sentiment_response: list[OpinionsSentiment],
) -> OpinionsSentimentAverage:
    average_sentiment = sum(
        opinion.sentiment for opinion in opinions_sentiment_response
    ) / len(opinions_sentiment_response)
    rounded_average_sentiment = round(average_sentiment, 2)
    return OpinionsSentimentAverage(value=rounded_average_sentiment)


def opinions_sentiment_request_list_to_str(
    opinions_list: list[Opinion],
):
    formatted_opinions = ", ".join(
        f"{opinion.id}: {opinion.content}" for opinion in opinions_list
    )
    return formatted_opinions


async def opinions_csv_to_list(file: UploadFile) -> list[Opinion]:
    content = await file.read()
    text = content.decode("utf-8")

    reader = csv.reader(io.StringIO(text))

    opinions_list = [Opinion(id=row[0], content=row[1]) for row in reader if row]

    return opinions_list
