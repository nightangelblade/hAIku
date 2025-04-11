import os


class ENVARS:
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    GEMINI_API_KEY: str
    REPO_PATH: str
    DEBUG_MODE: str
    
    def get_list(self):
        """Return a list of all column names."""
        return [
            self.OPENAI_API_KEY,
            self.ANTHROPIC_API_KEY,
            self.GEMINI_API_KEY,
            self.REPO_PATH,
            self.DEBUG_MODE,
        ]
    
def is_directory(path):
    return os.path.isdir(path)


def is_git_repo(path):
    return os.path.isdir(os.path.join(path, ".git"))


def read_last_n_words_from_file(file_path, n, chunk_size=4096):
    with open(file_path, 'rb') as f:
        f.seek(0, 2)  # Seek to end
        file_size = f.tell()
        buffer = b''

        pos = file_size
        while pos > 0:
            read_size = min(chunk_size, pos)
            pos -= read_size
            f.seek(pos)
            chunk = f.read(read_size)
            buffer = chunk + buffer

            if buffer.count(b',') >= n:
                break  # we have enough commas to extract n words

        # Now decode and split
        text = buffer.decode('utf-8', errors='ignore').strip(', \n\r')
        all_words = text.split(',')

        return all_words[-n:] if len(all_words) >= n else all_words
