from flask import Blueprint, jsonify

from service import AnalyticsService

analytics_bp = Blueprint(
    "analytics",
    __name__,
)

service = AnalyticsService()


@analytics_bp.get("/analytics/dashboard/<repository_name>")
def dashboard(repository_name):

    result = service.dashboard(repository_name)

    if result is None:

        return jsonify(
            {"error": "Repository not found"}
        ), 404

    return jsonify(result)

@analytics_bp.get("/analytics/rankings")
def rankings():

    return jsonify(
        service.rankings()
    )