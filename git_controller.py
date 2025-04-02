import git


class GitController:
    def __init__(self, directory_path, main_branch_name, remote_name):
        self.repo = git.Repo(directory_path)
        self.main_branch_name = main_branch_name
        self.remote_name = remote_name

    def add_files_and_commit_branch(self, updated_files, commit_message):
        for updated_file in updated_files:
            self.repo.index.add(updated_file)

        self.repo.index.commit(commit_message)

    def checkout_feature_branch(self, branch_name):
        self.repo.git.checkout(self.main_branch_name)
        self.repo.git.pull(self.remote_name, self.main_branch_name)
        self.repo.git.checkout("-b", branch_name)

    def push_branch(self, branch_name):
        self.repo.git.push("origin", branch_name)

    def auto_branch(self, branch_name, filenames, commit_message):
        self.checkout_feature_branch(branch_name)
        self.add_files_and_commit_branch(filenames, commit_message)
        self.push_branch(branch_name)
