import git
import os


def is_directory(path):
    return os.path.isdir(path)


def is_git_repo(path):
    return os.path.isdir(os.path.join(path, ".git"))
