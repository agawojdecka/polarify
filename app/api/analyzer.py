import json

from fastapi import APIRouter
from google import genai
from google.genai import types

from app.services.prompt import get_prompt

router = APIRouter()

client = genai.Client()


@router.post("/analyzer")
async def analyze(opinion: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Return polarity value (from -1.0 to +1.0) "
        f"of this opinion: '{opinion}'",
    )

    return {"Polarity": response.text}


@router.post("/analyzer-advanced")
async def analyze_advanced(opinions_dict: dict[str, str]):
    formatted_opinions = [f"{key}: {value}" for key, value in opinions_dict.items()]

    opinions_str = ", ".join(formatted_opinions)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"I will provide you with a set of opinions in the following format: "
        f"id: text, id: text, etc. Analyze each opinion and, in your response, "
        f"return the polarity (sentiment) of each opinion (from -1.0 negative "
        f"to +1.0 positive) using sentiment analysis tools. The response should be "
        f"in a similar format: id: polarity, id: polarity, etc... . Attention! "
        f"Do not provide any additional information/comments. You must return "
        f"only and exclusively the structure I provided in the response. "
        f"Here are the opinions: {opinions_str}",
    )
    if response.text is None:
        return {"Message": "Something went wrong."}
    else:
        items = response.text.split(", ")

        result_dict = {
            key: float(value_str)
            for item in items
            for key, value_str in (item.split(": "),)
        }

        return result_dict


@router.post("/analyzer-advanced-config")
async def analyze_advanced_config(opinions_dict: dict[str, str]):
    formatted_opinions = [f"{key}: {value}" for key, value in opinions_dict.items()]

    opinions_str = ", ".join(formatted_opinions)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=get_prompt("content.txt") + opinions_str,
            config=types.GenerateContentConfig(
                system_instruction=get_prompt("system_instructions.txt"),
                response_mime_type='application/json',
            ),
        )

        if response.text is None:
            return {"Message": "Something went wrong."}
        else:
            return json.loads(response.text)

    except Exception as e:
        print(f"An error occurred during API call: {e}")
        return None
