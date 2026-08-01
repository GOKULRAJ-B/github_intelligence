from datetime import datetime, date

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from database.db import SessionLocal
from database.models import (
    Repository,
    Contributor,
    Commit,
    PullRequest,
    DailyMetric,
    FileHotspot,
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

        contributor = Contributor(username=username)

        session.add(contributor)
        session.flush()

        return contributor

    def get_or_create_daily_metric(self, session, repository):

        today = date.today()

        metric = (
            session.query(DailyMetric)
            .filter(
                DailyMetric.repository_id == repository.id,
                func.date(DailyMetric.metric_date) == today,
            )
            .first()
        )

        if metric:
            return metric

        metric = DailyMetric(
            repository_id=repository.id,
            metric_date=datetime.utcnow(),
            total_commits=0,
            merged_prs=0,
            open_prs=0,
            avg_merge_time=0,
            active_contributors=0,
        )

        session.add(metric)
        session.flush()

        return metric

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
                commit["repository"],
            )

            contributor = self.get_or_create_contributor(
                session,
                commit["author"],
            )

            timestamp = None

            if commit["timestamp"]:

                timestamp = datetime.fromisoformat(
                    commit["timestamp"].replace(
                        "Z",
                        "+00:00",
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
            session.flush()

            metric = self.get_or_create_daily_metric(
                session,
                repository,
            )

            metric.total_commits += 1

            session.commit()

            print(f"Saved commit {commit['commit_id']}")
            print(f"Daily commits: {metric.total_commits}")

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

    def save_pull_request(self, pr):

        session = SessionLocal()

        try:

            repository = self.get_or_create_repository(
                session,
                pr["repository"],
            )

            contributor = self.get_or_create_contributor(
                session,
                pr["author"],
            )

            existing = (
                session.query(PullRequest)
                .filter_by(
                    pr_number=pr["pr_number"],
                    repository_id=repository.id,
                )
                .first()
            )

            if existing:

                print(
                    f"Pull Request #{pr['pr_number']} already exists"
                )

                return

            created_at = None
            merged_at = None
            closed_at = None

            if pr["created_at"]:

                created_at = datetime.fromisoformat(
                    pr["created_at"].replace(
                        "Z",
                        "+00:00",
                    )
                )

            if pr["merged_at"]:

                merged_at = datetime.fromisoformat(
                    pr["merged_at"].replace(
                        "Z",
                        "+00:00",
                    )
                )

            if pr["closed_at"]:

                closed_at = datetime.fromisoformat(
                    pr["closed_at"].replace(
                        "Z",
                        "+00:00",
                    )
                )

            db_pr = PullRequest(
                pr_number=pr["pr_number"],
                repository_id=repository.id,
                contributor_id=contributor.id,
                title=pr["title"],
                state=pr["state"],
                created_at=created_at,
                merged_at=merged_at,
                closed_at=closed_at,
                merge_time_minutes=pr["merge_time_minutes"],
            )

            session.add(db_pr)
            session.flush()

            metric = self.get_or_create_daily_metric(
                session,
                repository,
            )

            if (
                pr["state"] == "closed"
                and pr["merged_at"]
            ):

                metric.merged_prs += 1

            elif pr["state"] == "open":

                metric.open_prs += 1

            merged_prs = (
                session.query(PullRequest)
                .filter(
                    PullRequest.repository_id == repository.id,
                    PullRequest.merge_time_minutes.isnot(None),
                )
                .all()
            )

            if merged_prs:

                metric.avg_merge_time = int(
                    sum(
                        p.merge_time_minutes
                        for p in merged_prs
                    )
                    / len(merged_prs)
                )

            session.commit()

            print(
                f"Saved PR #{pr['pr_number']}"
            )

            print(
                f"Merged PRs : {metric.merged_prs}"
            )

            print(
                f"Open PRs   : {metric.open_prs}"
            )

            print(
                f"Avg Merge  : {metric.avg_merge_time}"
            )

        except IntegrityError:

            session.rollback()

            print(
                f"Duplicate PR #{pr['pr_number']}"
            )

        except Exception as e:

            session.rollback()

            print(f"Database Error: {e}")

            raise

        finally:

            session.close()
    
    def save_hotspot(self, file):

        session = SessionLocal()

        try:

            repository = self.get_or_create_repository(
                session,
                file["repository"],
            )

            hotspot = (
                session.query(FileHotspot)
                .filter_by(
                    repository_id=repository.id,
                    file_path=file["file_path"],
                )
                .first()
            )

            if hotspot:

                hotspot.commit_count += 1

            else:

                hotspot = FileHotspot(
                    repository_id=repository.id,
                    file_path=file["file_path"],
                    commit_count=1,
                )

                session.add(hotspot)

            session.commit()

            print(
                f"{file['file_path']} -> {hotspot.commit_count}"
            )

        except Exception as e:

            session.rollback()

            print(f"Database Error: {e}")

            raise

        finally:

            session.close()