import logging
from lib import read_last_n_words_from_file


class PromptGenerator:
    def __init__(self, haiku_themes_file_path):
        self.haiku_themes_file_path = haiku_themes_file_path

    def get_haiku_input_content_prompt(self) -> str:
        prompt = "Generate one haiku. Follow 5-7-5 syllable format."
        try:
            sub_themes_list = read_last_n_words_from_file(self.haiku_themes_file_path, 27)
            logging.debug(f"sub themes word list, number of items read into mem: {len(sub_themes_list)}")
            if sub_themes_list:
                prompt += " The haiku should not be derived from these topics: "
                sub_themes_str = ", ".join(sub_themes_list)
                prompt += sub_themes_str
                prompt += "."

        except Exception as e:
            logging.warning(f"Error when reading from themes file: {e}")

        prompt += " Also generate three related theme words separated by a comma."

        logging.debug(f"Base Prompt Provided:\n'{prompt}'")
        return prompt