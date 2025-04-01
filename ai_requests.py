from openai import OpenAI
import anthropic
import google.generativeai as genai
import logging


def get_gpt_haiku(OPENAI_API_KEY: str) -> list:
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": "write a haiku"}],
    )

    completion_list = completion.choices[0].message.content.split("\n")
    completion_list = [line.rstrip() for line in completion_list]
    return completion_list


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
