import os
from dotenv import load_dotenv
from openai import OpenAI
from git_controller import GitController
from datetime import datetime
import csv
import anthropic

class OutputCSVColumns:
    SOURCE = "source"
    DATE = "date"
    LINE_1 = "line_1"
    LINE_2 = "line_2"
    LINE_3 = "line_3"

    @classmethod
    def all_columns(cls):
        """Return a list of all column names."""
        return [
            cls.SOURCE,
	    cls.DATE,
            cls.LINE_1,
            cls.LINE_2,
            cls.LINE_3,
        ]



# Setup dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
REPO_PATH = os.getenv("REPO_PATH")

HAIKU_ROWS = []
DELIMITER = "|"

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

gpt_haiku = get_gpt_haiku()
GPT_ROWS = {OutputCSVColumns.SOURCE: "GPT", OutputCSVColumns.DATE: datetime.now().isoformat(), OutputCSVColumns.LINE_1: gpt_haiku[0], OutputCSVColumns.LINE_2: gpt_haiku[1], OutputCSVColumns.LINE_3: gpt_haiku[2]}
print(GPT_ROWS)

def get_anthropic_haiku() -> list:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model = "claude-3-5-haiku-20241022",
        max_tokens = 40,
        system="Respond with ONLY a haiku - 3 lines with 5, 7, and 5 syllables. No introduction or extra text.",
        messages=[
            {"role": "user", "content": "Write a haiku"}
        ]
    )

    message_list = message.content[0].text.split("\n")
    return message_list

anthropic_haiku = get_anthropic_haiku()
ANTHROPIC_ROWS = {OutputCSVColumns.SOURCE: "Anthropic", OutputCSVColumns.DATE: datetime.now().isoformat(), OutputCSVColumns.LINE_1: anthropic_haiku[0], OutputCSVColumns.LINE_2: anthropic_haiku[1], OutputCSVColumns.LINE_3: anthropic_haiku[2]}
print(ANTHROPIC_ROWS)

HAIKU_ROWS.append(GPT_ROWS)
HAIKU_ROWS.append(ANTHROPIC_ROWS)

def save_csv_data(csv_file_path, fieldnames, rows, delimiter):
    datetime_now = datetime.now().isoformat()

    with open(
        csv_file_path, "a", encoding="utf-8", newline=""
    ) as csvfile:  # Note: "a" for append mode opens for writing and creates file if doesn't exist
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=delimiter,
            quoting=csv.QUOTE_MINIMAL,
        )

        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        for row in rows:
            writer.writerow(row)

save_csv_data("haikus.csv", OutputCSVColumns.all_columns(), HAIKU_ROWS, DELIMITER)

git_controller = GitController(REPO_PATH)
