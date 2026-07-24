from django.db import transaction

from .models import Team, TeamMember


@transaction.atomic
def create_team(
    *,
    organization,
    name,
    description,
    lead,
):
    team = Team.objects.create(
        organization=organization,
        name=name,
        description=description,
        lead=lead,
    )

    TeamMember.objects.create(
        team=team,
        user=lead,
        role=TeamMember.Role.LEAD,
    )

    return team


@transaction.atomic
def add_team_member(
    *,
    team,
    user,
    role=TeamMember.Role.ENGINEER,
):
    return TeamMember.objects.create(
        team=team,
        user=user,
        role=role,
    )