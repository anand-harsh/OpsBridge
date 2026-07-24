from .models import Incident


def list_incidents(user):
    return (
        Incident.objects.filter(
            organization__memberships__user=user
        )
        .select_related(
            "organization",
            "service",
            "commander",
            "created_by",
        )
        .distinct()
        .order_by("-created_at")
    )


def get_incident(pk):
    return Incident.objects.select_related(
        "organization",
        "service",
        "commander",
        "created_by",
    ).get(pk=pk)