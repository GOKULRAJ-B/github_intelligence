from datetime import datetime


def parse_pr_event(event):

    repository = event["repository"]["name"]

    pr = event["pull_request"]

    merged_at = pr.get("merged_at")
    created_at = pr.get("created_at")
    closed_at = pr.get("closed_at")

    merge_minutes = None

    if created_at and merged_at:

        created = datetime.fromisoformat(
            created_at.replace("Z", "+00:00")
        )

        merged = datetime.fromisoformat(
            merged_at.replace("Z", "+00:00")
        )

        merge_minutes = int(
            (merged - created).total_seconds() / 60
        )

    return {

        "repository": repository,

        "pr_number": pr["number"],

        "author": pr["user"]["login"],

        "title": pr["title"],

        "state": pr["state"],

        "created_at": created_at,

        "merged_at": merged_at,

        "closed_at": closed_at,

        "merge_time_minutes": merge_minutes,
    }