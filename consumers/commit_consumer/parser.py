def parse_push_event(event):

    repository = event.get("repository", {}).get("name")

    commits = event.get("commits", [])

    parsed = []

    for commit in commits:

        parsed.append(
            {
                "repository": repository,
                "commit_id": commit.get("id"),
                "message": commit.get("message"),
                "author": commit.get("author", {}).get("name"),
                "timestamp": commit.get("timestamp"),
            }
        )

    return parsed