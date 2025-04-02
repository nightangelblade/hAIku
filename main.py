import os
import logging
from dotenv import load_dotenv
from git_controller import GitController
from datetime import datetime
from csv_lib import OutputCSVColumns, save_csv_data
from ai_requests import get_gpt_haiku, get_anthropic_haiku, get_gemini_haiku
from site_generator import SiteGenerator
from lib import is_directory, is_git_repo

if __name__ == "__main__":
    # Setup logger
    logging.basicConfig(
        level=logging.WARNING,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
        handlers=[
            logging.StreamHandler(),  # Print to console
            logging.FileHandler("error.log"),  # Save to a file
        ],
    )

    # Setup dotenv and retrieve env varas
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    REPO_PATH = os.getenv("REPO_PATH")

    env_vars = [OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, REPO_PATH]
    for idx, var in enumerate(env_vars):
        if not var:
            logging.critical(f"Missing ENV VAR: '{idx}'")
            exit(1)  # Quit program

    if not is_directory(REPO_PATH):
        logging.critical(f"Path is not a directory: '{REPO_PATH}'")
        exit(1)

    if not is_git_repo(REPO_PATH):
        logging.critical(f"Path is not a git repository: '{REPO_PATH}'")
        exit(1)

    # Preparations for git push
    branch_name = "auto_haiku_generate" + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
    update_filenames = ["haikus.csv", "index.html"]
    commit_message = "Automatic commit. Haikus generated and static webpage updated"
    git_controller = GitController(REPO_PATH, "test_git_master", "origin")

    HAIKU_ROWS = []
    DELIMITER = "|"

    try:
        gpt_haiku = get_gpt_haiku(OPENAI_API_KEY)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)

    GPT_ROWS = {
        OutputCSVColumns.SOURCE: "GPT",
        OutputCSVColumns.DATE: datetime.now().isoformat(),
        OutputCSVColumns.LINE_1: gpt_haiku[0],
        OutputCSVColumns.LINE_2: gpt_haiku[1],
        OutputCSVColumns.LINE_3: gpt_haiku[2],
    }
    logging.debug(GPT_ROWS)

    try:
        anthropic_haiku = get_anthropic_haiku(ANTHROPIC_API_KEY)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)

    ANTHROPIC_ROWS = {
        OutputCSVColumns.SOURCE: "Anthropic",
        OutputCSVColumns.DATE: datetime.now().isoformat(),
        OutputCSVColumns.LINE_1: anthropic_haiku[0],
        OutputCSVColumns.LINE_2: anthropic_haiku[1],
        OutputCSVColumns.LINE_3: anthropic_haiku[2],
    }
    logging.debug(ANTHROPIC_ROWS)

    try:
        gemini_haiku = get_gemini_haiku(GEMINI_API_KEY)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)

    GEMINI_ROWS = {
        OutputCSVColumns.SOURCE: "Gemini",
        OutputCSVColumns.DATE: datetime.now().isoformat(),
        OutputCSVColumns.LINE_1: gemini_haiku[0],
        OutputCSVColumns.LINE_2: gemini_haiku[1],
        OutputCSVColumns.LINE_3: gemini_haiku[2],
    }

    HAIKU_ROWS.append(GPT_ROWS)
    HAIKU_ROWS.append(ANTHROPIC_ROWS)
    HAIKU_ROWS.append(GEMINI_ROWS)

    save_csv_data("haikus.csv", OutputCSVColumns.all_columns(), HAIKU_ROWS, DELIMITER)

    # generate static site
    site_generator = SiteGenerator(haikus=HAIKU_ROWS)
    site_generator.generate()

    # Push to Github
    try:
        git_controller.auto_branch(branch_name, update_filenames, commit_message)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)
