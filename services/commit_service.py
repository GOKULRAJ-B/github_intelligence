from database.repository import RepositoryService


class CommitService:

    def __init__(self, repository: RepositoryService):
        self.repository = repository

    def process_commits(self, commits):

        for commit in commits:

            self.repository.save_commit(commit)