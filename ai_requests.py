from openai import OpenAI
import anthropic
from google import genai
from csv_lib import OutputCSVColumns
from pydantic import create_model
import logging
import json


def get_gpt_haiku(OPENAI_API_KEY: str, prompt: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        input=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini-2024-07-18",
        text={
            "format": {
                "type": "json_schema",
                "name": "haiku_lines",
                "schema": {
                    "type": "object",
                    "properties": {
                        OutputCSVColumns.LINE_1: {"type": "string"},
                        OutputCSVColumns.LINE_2: {"type": "string"},
                        OutputCSVColumns.LINE_3: {"type": "string"},
                        "themes": {"type": "string"},
                    },
                    "required": [
                        OutputCSVColumns.LINE_1,
                        OutputCSVColumns.LINE_2,
                        OutputCSVColumns.LINE_3,
                        "themes",
                    ],
                    "additionalProperties": False,
                },
                "strict": True,
            }
        },
        store=True,
    )
    haiku_response = json.loads(response.output_text)
    return haiku_response


def get_anthropic_haiku(ANTHROPIC_API_KEY: str, prompt: str) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    haiku_response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=500,
        system="You are a haiku generator that creates haikus and provides three theme words that describe each haiku. Always include both the haiku and its theme words.",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        tools=[
            {
                "name": "get_haiku",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        OutputCSVColumns.LINE_1: {
                            "type": "string",
                            "description": "First line of the haiku (5 syllables)",
                        },
                        OutputCSVColumns.LINE_2: {
                            "type": "string",
                            "description": "Second line of the haiku (7 syllables)",
                        },
                        OutputCSVColumns.LINE_3: {
                            "type": "string",
                            "description": "Third line of the haiku (5 syllables)",
                        },
                        "themes": {
                            "type": "string",
                            "description": "IMPORTANT: Three descriptive theme words separated by commas.",
                        },
                    },
                    "required": [
                        OutputCSVColumns.LINE_1,
                        OutputCSVColumns.LINE_2,
                        OutputCSVColumns.LINE_3,
                        "themes",
                    ],
                },
            }
        ],
        tool_choice={"type": "tool", "name": "get_haiku"},
    )
    return haiku_response.content[0].input


def get_gemini_haiku(GEMINI_API_KEY: str, prompt: str) -> dict:
    Haiku = create_model(
        "Haiku",
        **{
            OutputCSVColumns.LINE_1: (str, ...),
            OutputCSVColumns.LINE_2: (str, ...),
            OutputCSVColumns.LINE_3: (str, ...),
            "themes": (str, ...),
        }
    )

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Haiku,
        },
    )

    return json.loads(response.text)
