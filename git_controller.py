import git


class GitController:
    def __init__(self, directory_path):
        self.repo = git.Repo(directory_path)

    def commit_branch(self):
        self.repo.index.add(haikus.csv)
        print("Updated haiku file added to commit")
        self.repo.index.commit("Created new haikus for poets")
        print("Commit Created")

    def checkout_branch(self, branch_name):
        current_branch = self.repo.heads[branch_name]
        current_branch.checkout()
        print("Branch Checked Out: ", current_branch)

    def push_branch(self, branch_name):
        self.repo.git.push("origin", branch_name)
        print("Branch Pushed to Origin")

    def auto_branch(self, branch_name):
        self.checkout_branch(branch_name)
        self.commit_branch()
        self.push_branch(branch_name)
