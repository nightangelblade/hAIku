from openai import OpenAI
import anthropic
import google.generativeai as genai
from csv_lib import OutputCSVColumns
import logging
import json


def get_gpt_haiku(OPENAI_API_KEY: str) -> list:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        input=[
            {
                "role": "user",
                "content": "write a haiku and give me three words that describe it",
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


def get_anthropic_haiku(ANTHROPIC_API_KEY: str) -> list:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=40,
        system="Respond with ONLY a haiku - 3 lines with 5, 7, and 5 syllables. No introduction or extra text.",
        messages=[{"role": "user", "content": "Write a haiku"}],
    )

    message_list = message.content[0].text.split("\n")
    return message_list


def get_gemini_haiku(GEMINI_API_KEY: str) -> list:
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    prompt = "Generate one haiku. Follow 5-7-5 syllable format."
    response = model.generate_content(prompt)
    response = response.text.rstrip()
    return response.split("\n")
