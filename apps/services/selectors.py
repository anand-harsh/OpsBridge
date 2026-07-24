from .models import Service


def list_services_for_user(user):
    return (
        Service.objects.filter(
            organization__memberships__user=user,
            is_active=True,
        )
        .select_related(
            "organization",
            "team",
        )
        .distinct()
    )


def get_service(service_id):
    return Service.objects.select_related(
        "organization",
        "team",
    ).get(id=service_id)