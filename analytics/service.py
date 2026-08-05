from database.db import SessionLocal
from database.models import (
    DailyMetric,
    Repository,
)
from database.models import DeveloperRanking, Contributor

class AnalyticsService:

    def dashboard(self, repository_name):

        session = SessionLocal()

        try:

            repository = (
                session.query(Repository)
                .filter_by(name=repository_name)
                .first()
            )

            if not repository:
                return None

            metric = (
                session.query(DailyMetric)
                .filter_by(repository_id=repository.id)
                .order_by(
                    DailyMetric.metric_date.desc()
                )
                .first()
            )

            if not metric:
                return {}

            return {
                "repository": repository.name,
                "total_commits": metric.total_commits,
                "merged_prs": metric.merged_prs,
                "open_prs": metric.open_prs,
                "average_merge_time": metric.avg_merge_time,
                "active_contributors": metric.active_contributors,
            }

        finally:

            session.close()




    def rankings(self):

        session = SessionLocal()

        try:

            rankings = (
                session.query(
                    Contributor.username,
                    DeveloperRanking.total_commits,
                    DeveloperRanking.merged_prs,
                    DeveloperRanking.score,
                )
                .join(
                    Contributor,
                    Contributor.id == DeveloperRanking.contributor_id,
                )
                .order_by(
                    DeveloperRanking.score.desc()
                )
                .all()
            )

            result = []

            for row in rankings:

                result.append(
                    {
                        "developer": row.username,
                        "commits": row.total_commits,
                        "merged_prs": row.merged_prs,
                        "score": row.score,
                    }
                )

            return result

        finally:

            session.close()