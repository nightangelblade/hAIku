import os
from dotenv import load_dotenv
from openai import OpenAI
from git_controller import GitController

# Setup dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_PATH = os.getenv("REPO_PATH")

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[{"role": "user", "content": "write a haiku"}],
)

print(completion.choices[0].message)

git_controller = GitController(REPO_PATH)
