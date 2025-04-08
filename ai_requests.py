from openai import OpenAI
import anthropic
import google.generativeai as genai
import logging
import json


def get_gpt_haiku(OPENAI_API_KEY: str) -> list:
    client = OpenAI(api_key=OPENAI_API_KEY)
    function_definitions = [
        {
            "name": "return_haiku",
            "description": "Returns a haiku in three lines followed by a fourth line containing three descriptive words.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lines": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "An array of four strings: Three haiku lines followed by a fourth line containing exactly three words that describe the haiku.",
                    }
                },
                "required": ["lines"],
            },
        }
    ]

    messages = [
        {
            "role": "user",
            "content": "Write a haiku and provide three words that best describe its mood or theme. Return them as four separate lines in total.",
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        functions=function_definitions,
        function_call={"name": "return_haiku"},  # Forces the model to use this function
    )

    args = response.choices[0].message.function_call.arguments
    parsed = json.loads(args)

    return parsed["lines"]


def get_anthropic_haiku(ANTHROPIC_API_KEY: str) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=100,
        system="You must respond ONLY with a valid JSON object. No explanations or other text. Generate a haiku with 3 lines (5-7-5 syllable pattern) and provide 3 descriptive tags. The JSON should have 'haiku' (array of 3 strings) and 'tags' (array of 3 strings) keys.",
        messages=[{"role": "user", "content": "Write a haiku"}],
    )

    try:
        response = json.loads(message.content[0].text)
        tags_string = ", ".join(response["tags"])
        final_response = response["haiku"] + [tags_string]
        return final_response
    except json.JSONDecodeError:
        # If parsing fails, return the raw text
        return {"error": "Failed to parse JSON", "raw_text": message.content[0].text}


def get_gemini_haiku(GEMINI_API_KEY: str) -> list:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    prompt = """Generate a haiku following 5-7-5 syllable format. Then provide three descriptive tags for the haiku.

    Return your answer in valid JSON format with this exact structure:
    {
      "haiku": ["line1", "line2", "line3"],
      "tags": ["tag1", "tag2", "tag3"]
    }

    Return ONLY the JSON with no markdown formatting, no code blocks, and no other text."""

    response = model.generate_content(prompt)
    response_text = response.text.strip()

    if response_text.startswith("```") and response_text.endswith("```"):
        # Remove opening and closing code block markers
        response_text = response_text.split("```")[1]

    if response_text.startswith("json\n"):
        response_text = response_text[5:]

    response_text = response_text.strip()

    try:
        json_response = json.loads(response_text)

        tags_string = ", ".join(json_response["tags"])

        final_response = json_response["haiku"] + [tags_string]
        return final_response
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {response_text}")
        return response_text.split("\n")
