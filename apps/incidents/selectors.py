from .models import Incident


def get_incident_by_id(incident_id):
    return Incident.objects.select_related(
        "organization",
        "service",
        "commander",
        "created_by",
    ).get(id=incident_id)


def list_open_incidents(organization):
    return (
        Incident.objects.filter(
            organization=organization,
            status__in=[
                Incident.Status.OPEN,
                Incident.Status.INVESTIGATING,
                Incident.Status.MONITORING,
            ],
        )
        .select_related(
            "service",
            "commander",
        )
        .order_by("-created_at")
    )