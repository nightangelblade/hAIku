import os
from dotenv import load_dotenv
from openai import OpenAI
from git_controller import GitController

# Setup dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_PATH = os.getenv("REPO_PATH")


def get_gpt_haiku() -> list:
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": "write a haiku"}],
    )

    completion_list = completion.choices[0].message.content.split("\n")
    completion_list = [line.rstrip() for line in completion_list]
    return completion_list

print(get_gpthaiku())

git_controller = GitController(REPO_PATH)
