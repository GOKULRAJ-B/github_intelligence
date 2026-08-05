def parse_push_event(event):

    return {
        "repository": event["repository"]["name"]
    }