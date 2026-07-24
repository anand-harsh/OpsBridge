from django.db import transaction

from .models import Service


@transaction.atomic
def create_service(
    *,
    organization,
    team,
    name,
    description=""
):
    if team.organization_id != organization.id:
        raise ValueError("Selected team does not belong to this organization.")

    return Service.objects.create(
        organization=organization,
        team=team,
        name=name,
        description=description,
    )