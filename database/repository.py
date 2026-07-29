from datetime import datetime

from sqlalchemy.exc import IntegrityError

from database.db import SessionLocal
from database.models import (
    Repository,
    Contributor,
    Commit,
)


class RepositoryService:

    def get_or_create_repository(self, session, name):

        repo = (
            session.query(Repository)
            .filter_by(name=name)
            .first()
        )

        if repo:
            return repo

        repo = Repository(name=name)

        session.add(repo)

        session.flush()

        return repo

    def get_or_create_contributor(self, session, username):

        contributor = (
            session.query(Contributor)
            .filter_by(username=username)
            .first()
        )

        if contributor:
            return contributor

        contributor = Contributor(
            username=username
        )

        session.add(contributor)

        session.flush()

        return contributor

    def save_commit(self, commit):

        session = SessionLocal()

        try:

            existing = (
                session.query(Commit)
                .filter_by(commit_sha=commit["commit_id"])
                .first()
            )

            if existing:

                print(
                    f"Commit already exists: {commit['commit_id']}"
                )

                return

            repository = self.get_or_create_repository(
                session,
                commit["repository"]
            )

            contributor = self.get_or_create_contributor(
                session,
                commit["author"]
            )

            timestamp = None

            if commit["timestamp"]:

                timestamp = datetime.fromisoformat(
                    commit["timestamp"].replace(
                        "Z",
                        "+00:00"
                    )
                )

            db_commit = Commit(
                commit_sha=commit["commit_id"],
                repository_id=repository.id,
                contributor_id=contributor.id,
                message=commit["message"],
                commit_time=timestamp,
            )

            session.add(db_commit)

            session.commit()

            print(
                f"Saved commit {commit['commit_id']}"
            )

        except IntegrityError:

            session.rollback()

            print(
                f"Duplicate commit: {commit['commit_id']}"
            )

        except Exception as e:

            session.rollback()

            print(f"Database Error: {e}")

            raise

        finally:

            session.close()