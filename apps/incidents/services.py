from django.db import transaction
from django.utils import timezone

from .models import Incident, IncidentEvent


@transaction.atomic
def create_incident(*, user, service, title, description, severity):

    incident = Incident.objects.create(
        organization=service.organization,
        service=service,
        title=title,
        description=description,
        severity=severity,
        commander=user,
        created_by=user,
    )

    IncidentEvent.objects.create(
        incident=incident,
        user=user,
        event_type=IncidentEvent.EventType.CREATED,
        message=f"{user.email} created the incident.",
    )

    return incident


@transaction.atomic
def change_severity(*, incident, severity, changed_by):

    old = incident.severity

    incident.severity = severity
    incident.save(update_fields=["severity"])

    IncidentEvent.objects.create(
        incident=incident,
        user=changed_by,
        event_type=IncidentEvent.EventType.SEVERITY_CHANGED,
        message=f"Severity changed from {old} to {severity}",
    )

    return incident


@transaction.atomic
def resolve_incident(*, incident, resolved_by):

    incident.status = Incident.Status.RESOLVED
    incident.resolved_at = timezone.now()

    incident.save(
        update_fields=[
            "status",
            "resolved_at",
        ]
    )

    IncidentEvent.objects.create(
        incident=incident,
        user=resolved_by,
        event_type=IncidentEvent.EventType.RESOLVED,
        message="Incident resolved.",
    )

    return incident