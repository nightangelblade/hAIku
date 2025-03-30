import os
import logging
from dotenv import load_dotenv
from git_controller import GitController
from datetime import datetime
from csv_lib import OutputCSVColumns, save_csv_data
from ai_requests import get_gpt_haiku, get_anthropic_haiku



if __name__ == "__main__":
    # Setup logger
    logging.basicConfig(
        level=logging.WARNING,                    # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        handlers=[
            logging.StreamHandler(),          # Print to console
            logging.FileHandler('error.log')    # Save to a file
        ]
    )

    # Setup dotenv and retrieve env varas
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    REPO_PATH = os.getenv("REPO_PATH")

    env_vars = [OPENAI_API_KEY, ANTHROPIC_API_KEY, REPO_PATH]
    for var in env_vars:
        if not var:
            logging.critical(f"Missing ENV VAR: '{var}'")
            exit(1) # Quit program
    

    HAIKU_ROWS = []
    DELIMITER = "|"

    try:
        gpt_haiku = get_gpt_haiku(OPENAI_API_KEY)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)

    GPT_ROWS = {OutputCSVColumns.SOURCE: "GPT", OutputCSVColumns.DATE: datetime.now().isoformat(), OutputCSVColumns.LINE_1: gpt_haiku[0], OutputCSVColumns.LINE_2: gpt_haiku[1], OutputCSVColumns.LINE_3: gpt_haiku[2]}
    logging.debug(GPT_ROWS)

    try:
        anthropic_haiku = get_anthropic_haiku(ANTHROPIC_API_KEY)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)

    ANTHROPIC_ROWS = {OutputCSVColumns.SOURCE: "Anthropic", OutputCSVColumns.DATE: datetime.now().isoformat(), OutputCSVColumns.LINE_1: anthropic_haiku[0], OutputCSVColumns.LINE_2: anthropic_haiku[1], OutputCSVColumns.LINE_3: anthropic_haiku[2]}
    logging.debug(ANTHROPIC_ROWS)

    HAIKU_ROWS.append(GPT_ROWS)
    HAIKU_ROWS.append(ANTHROPIC_ROWS)

    save_csv_data("haikus.csv", OutputCSVColumns.all_columns(), HAIKU_ROWS, DELIMITER)

    # git_controller = GitController(REPO_PATH)
