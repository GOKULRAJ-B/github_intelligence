from database.db import SessionLocal
from database.models import (
    Repository,
    Contributor,
    Commit,
    PullRequest,
    DeveloperRanking,
)


class RankingService:

    def update_ranking(self, repository_name):

        session = SessionLocal()

        try:

            repository = (
                session.query(Repository)
                .filter_by(name=repository_name)
                .first()
            )

            if not repository:
                return

            contributors = (
                session.query(Contributor)
                .all()
            )

            for contributor in contributors:

                commit_count = (
                    session.query(Commit)
                    .filter(
                        Commit.repository_id == repository.id,
                        Commit.contributor_id == contributor.id,
                    )
                    .count()
                )

                merged_prs = (
                    session.query(PullRequest)
                    .filter(
                        PullRequest.repository_id == repository.id,
                        PullRequest.contributor_id == contributor.id,
                        PullRequest.merged_at.isnot(None),
                    )
                    .count()
                )

                score = commit_count + (merged_prs * 5)

                ranking = (
                    session.query(DeveloperRanking)
                    .filter_by(
                        repository_id=repository.id,
                        contributor_id=contributor.id,
                    )
                    .first()
                )

                if ranking:

                    ranking.total_commits = commit_count
                    ranking.merged_prs = merged_prs
                    ranking.score = score

                else:

                    ranking = DeveloperRanking(
                        repository_id=repository.id,
                        contributor_id=contributor.id,
                        total_commits=commit_count,
                        merged_prs=merged_prs,
                        score=score,
                    )

                    session.add(ranking)

            session.commit()

            print("Developer rankings updated.")

        except Exception as e:

            session.rollback()
            print(e)
            raise

        finally:

            session.close()