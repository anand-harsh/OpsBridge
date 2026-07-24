from .models import Team


def get_team(team_id):
    return Team.objects.select_related(
        "organization",
        "lead",
    ).get(id=team_id)


def list_teams_for_user(user):
    return (
        Team.objects.filter(
            organization__memberships__user=user
        )
        .select_related(
            "organization",
            "lead",
        )
        .distinct()
        .order_by("name")
    )