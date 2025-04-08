import os
import logging
from dotenv import load_dotenv
from git_controller import GitController
from datetime import datetime
from csv_lib import OutputCSVColumns, save_csv_data
from ai_requests import get_gpt_haiku, get_anthropic_haiku, get_gemini_haiku
from site_generator import SiteGenerator
from lib import is_directory, is_git_repo
from prompt_generator import PromptGenerator

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

    # More global vars
    haikus_csv_file_path = "haikus.csv"
    haiku_themes_file_path = "haiku_themes.txt"

    # Error checking env vars
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
    update_filenames = ["haikus.csv", "haiku_themes.txt", "index.html"]
    commit_message = "Automatic commit. Haikus generated and static webpage updated"
    git_controller = GitController(REPO_PATH, "master", "origin")

    # Preparations for prompt generator
    prompt_generator = PromptGenerator(haiku_themes_file_path=haiku_themes_file_path)
    haiku_prompt = prompt_generator.get_haiku_input_content_prompt()

    # Request Haikus
    HAIKU_ROWS = []
    THEMES = []
    DELIMITER = "|"

    try:
        gpt_haiku = get_gpt_haiku(OPENAI_API_KEY, haiku_prompt)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)
    
    try:
        anthropic_haiku = get_anthropic_haiku(ANTHROPIC_API_KEY, haiku_prompt)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)

    try:
        gemini_haiku = get_gemini_haiku(GEMINI_API_KEY, haiku_prompt)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)

    sources = {
        "GPT": gpt_haiku,
        "Anthropic": anthropic_haiku,
        "Gemini": gemini_haiku
    }

    for key, value in sources.items():
        value[OutputCSVColumns.SOURCE] = key
        value[OutputCSVColumns.DATE] = datetime.now().isoformat()

        theme_word_raw = value['themes']
        for word in theme_word_raw.split(','):
            if word.strip():
                THEMES.append(word.strip())

        del value['themes']

        HAIKU_ROWS.append(value)


    # Saving CSV Data
    save_csv_data(haikus_csv_file_path, OutputCSVColumns.all_columns(), HAIKU_ROWS, DELIMITER)

    # Save Themes data
    with open(
        haiku_themes_file_path, "a", encoding="utf-8", newline=""
    ) as themes_file:  # Note: "a" for append mode opens for writing and creates file if doesn't exist
        themes_str = ",".join(THEMES)
        themes_file.write(themes_str)
        themes_file.write(",")


    # Site generation 
    # First format date time on haiku dates
    for haiku in HAIKU_ROWS:
        if haiku[OutputCSVColumns.DATE]:
            try:
                dt = datetime.fromisoformat(haiku[OutputCSVColumns.DATE])
                formatted = dt.strftime("%B %d, %Y at %I:%M:%S %p")
                haiku[OutputCSVColumns.DATE] = formatted
            except ValueError:
                logging.warning(f"Haiku date formatting failed for date: {haiku[OutputCSVColumns.DATE]}")
    # Generate static site
    site_generator = SiteGenerator(haikus=HAIKU_ROWS)
    site_generator.generate()


    # Push to Github
    try:
        git_controller.auto_branch(branch_name, update_filenames, commit_message)
    except Exception as e:
        logging.error(f"{e}")
        exit(1)
