import git


class GitController:
    def __init__(self, directory_path):
        self.repo = git.Repo(directory_path)

    def update_file(self, file):
        file_to_update = open(file, "r").read()

        haiku_generate = "haiku_placeholder"  # < Logic for generating haiku goes here >

        updated_file = open(test_file, "a").write(haiku_generate)
        return ("File Updated: ", file)

    def update_poets(self):
        poets = ["gpt.txt", "sonnet.txt", "gemini.txt"]
        poets_completed = [self.update_file(poet) for poet in poets]
        print("Files Updated: ", poets)

        self.repo.index.add(poets)
        print("Files Added to Index: ", poets)
        self.repo.index.commit("Created new haikus for poets")
        print("Commit Created")

    def push_branch(self, branch_name):
        current_branch = self.repo.heads[branch_name]
        current_branch.checkout()
        print("Branch Checked Out: ", current_branch)

        self.repo.git.push("origin", branch_name)
        print("Branch Pushed to Origin")


"""
directory_path = 'REPO_PATH' # to be updated
repo = git.Repo(directory_path)

gpt_file = 'gpt.txt'
sonnet_file = 'sonnet.txt'
gemini_file = 'gemini.txt'

def update_file(file):
    file_to_update = open(file, "r").read()

    haiku_generate = "haiku_placeholder" # < Logic for generating haiku goes here >

    updated_file = open(test_file, "a").write(haiku_generate)
    return "File Updated: ", file)

poets = [gpt_file, sonnet_file, gemini_file]
poets_completed = [update_file(poet) for poet in poets]
print('Files Updated: ', poets)

repo.index.add(poets)
print('Files Added to Index: ', poets)
repo.index.commit('Created new haikus for poets')
print('Commit Created')

branch_name = 'test'
current_branch = repo.heads[branch_name]

current_branch.checkout()
print('Branch Checked Out: ', current_branch)

repo.git.push('origin', branch_name)
print('Branch Pushed to Origin')
"""
