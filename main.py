import os
import logging
from dotenv import load_dotenv
from git_controller import GitController
from datetime import datetime
from csv_lib import OutputCSVColumns, save_csv_data
from ai_requests import get_gpt_haiku, get_anthropic_haiku, get_gemini_haiku
from site_generator import SiteGenerator
from lib import is_directory, is_git_repo, ENVARS
from prompt_generator import PromptGenerator
from typing import Tuple


class HaikuGen:
    def __init__(self, env_vars: ENVARS):
        self.env_vars = env_vars
        self.haikus_csv_file_path = "haikus.csv"
        self.haiku_themes_file_path = "haiku_themes.txt"

        # Preparations for prompt generator
        self.prompt_generator = PromptGenerator(haiku_themes_file_path=self.haiku_themes_file_path)
        # Init site generator
        self.site_generator = SiteGenerator()

    def get_haikus_and_themes(self, haiku_prompt) -> Tuple[list, list]:
        HAIKU_ROWS = []
        THEMES = []
        
        try:
            gpt_haiku = get_gpt_haiku(self.env_vars.OPENAI_API_KEY, haiku_prompt)
        except Exception as e:
            logging.error(f"{e}")
            exit(1)
        
        try:
            anthropic_haiku = get_anthropic_haiku(self.env_vars.ANTHROPIC_API_KEY, haiku_prompt)
        except Exception as e:
            logging.error(f"{e}")
            exit(1)

        try:
            gemini_haiku = get_gemini_haiku(self.env_vars.GEMINI_API_KEY, haiku_prompt)
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
        return (HAIKU_ROWS, THEMES)

    def save_data_to_file(self, HAIKU_ROWS: list, THEMES: list):
        DELIMITER = "|"
        # Saving CSV Data
        save_csv_data(self.haikus_csv_file_path, OutputCSVColumns.all_columns(), HAIKU_ROWS, DELIMITER)
        # Save Themes data
        with open(
            self.haiku_themes_file_path, "a", encoding="utf-8", newline=""
        ) as themes_file:  # Note: "a" for append mode opens for writing and creates file if doesn't exist
            themes_str = ",".join(THEMES)
            themes_file.write(themes_str)
            themes_file.write(",")  

    def generate_static_site(self, HAIKU_ROWS: list):
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
        self.site_generator.generate_haiku_index(HAIKU_ROWS)

    def github_auto_branching(self):
        # Preparations for git push
        branch_name = "auto_haiku_generate" + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
        update_filenames = ["haikus.csv", "haiku_themes.txt", "index.html"]
        commit_message = "Automatic commit. Haikus generated and static webpage updated"
        git_controller = GitController(self.env_vars.REPO_PATH, "show", "origin")
        # Push to Github
        try:
            git_controller.auto_branch(branch_name, update_filenames, commit_message)
        except Exception as e:
            logging.error(f"{e}")
            exit(1)

    def run_process(self):
        haiku_prompt = self.prompt_generator.get_haiku_input_content_prompt()
        (HAIKU_ROWS, THEMES) = self.get_haikus_and_themes(haiku_prompt)
        self.save_data_to_file(HAIKU_ROWS, THEMES)
        self.generate_static_site(HAIKU_ROWS)
        if not self.env_vars.DEBUG_MODE:
            self.github_auto_branching()


if __name__ == "__main__":
    load_dotenv()
        
    # Setup dotenv and retrieve env varas
    env_vars = ENVARS()
    env_vars.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    env_vars.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    env_vars.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    env_vars.REPO_PATH = os.getenv("REPO_PATH")

    DEBUG_MODE = os.getenv("DEBUG_MODE")

    if DEBUG_MODE == "True":
        DEBUG_MODE = True
    elif DEBUG_MODE == "False":
        DEBUG_MODE = False
    else:
        # Default to True
        DEBUG_MODE = True
    env_vars.DEBUG_MODE = DEBUG_MODE

    if DEBUG_MODE:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.WARNING

        # Setup logger
    logging.basicConfig(
        level=logging.WARNING,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
        handlers=[
            logging.StreamHandler(),  # Print to console
            logging.FileHandler("error.log"),  # Save to a file
        ],
    )

    # Error checking env vars
    env_vars_list = env_vars.get_list()
    for idx, var in enumerate(env_vars_list):
        if var is None:
            logging.critical(f"Missing ENV VAR: '{idx}'")
            exit(1)  # Quit program

    if not is_directory(env_vars.REPO_PATH):
        logging.critical(f"Path is not a directory: '{env_vars.REPO_PATH}'")
        exit(1)

    if not is_git_repo(env_vars.REPO_PATH):
        logging.critical(f"Path is not a git repository: '{env_vars.REPO_PATH}'")
        exit(1)

    haiku_gen = HaikuGen(env_vars)
    haiku_gen.run_process()