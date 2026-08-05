from datetime import datetime

from database.db import SessionLocal
from database.models import (
    Repository,
    Contributor,
    Commit,
    DeveloperChurn,
)


class ChurnService:

    def update_churn(self, repository_name):

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

                latest_commit = (
                    session.query(Commit)
                    .filter(
                        Commit.repository_id == repository.id,
                        Commit.contributor_id == contributor.id,
                    )
                    .order_by(
                        Commit.commit_time.desc()
                    )
                    .first()
                )

                if not latest_commit:
                    continue

                inactive_days = (
                    datetime.utcnow() - latest_commit.commit_time.replace(tzinfo=None)
                ).days

                status = (
                    "Inactive"
                    if inactive_days > 30
                    else "Active"
                )

                churn = (
                    session.query(DeveloperChurn)
                    .filter_by(
                        repository_id=repository.id,
                        contributor_id=contributor.id,
                    )
                    .first()
                )

                if churn:

                    churn.last_commit = latest_commit.commit_time
                    churn.inactive_days = inactive_days
                    churn.status = status

                else:

                    churn = DeveloperChurn(
                        repository_id=repository.id,
                        contributor_id=contributor.id,
                        last_commit=latest_commit.commit_time,
                        inactive_days=inactive_days,
                        status=status,
                    )

                    session.add(churn)

            session.commit()

            print("Developer churn updated.")

        except Exception as e:

            session.rollback()

            print(e)

            raise

        finally:

            session.close()