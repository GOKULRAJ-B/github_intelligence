from database.repository import RepositoryService


class PRService:

    def __init__(self, repository: RepositoryService):
        self.repository = repository

    def process_pr(self, pr):

        self.repository.save_pull_request(pr)