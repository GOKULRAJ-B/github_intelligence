def parse_push_event(event):

    repository = event.get("repository", {}).get("name")

    commits = event.get("commits", [])

    files = []

    for commit in commits:

        for file in commit.get("added", []):
            files.append(
                {
                    "repository": repository,
                    "file_path": file,
                }
            )

        for file in commit.get("modified", []):
            files.append(
                {
                    "repository": repository,
                    "file_path": file,
                }
            )

        for file in commit.get("removed", []):
            files.append(
                {
                    "repository": repository,
                    "file_path": file,
                }
            )

    return files