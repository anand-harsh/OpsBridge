from django.db import transaction

from .models import Incident, IncidentEvent
from django.utils import timezone

@transaction.atomic
def create_incident(*, user, **validated_data):

    incident = Incident.objects.create(
        created_by=user,
        commander=user,
        **validated_data,
    )

    IncidentEvent.objects.create(
        incident=incident,
        user=user,
        event_type=IncidentEvent.EventType.CREATED,
        message=f"{user.email} created the incident.",
    )

    return incident

@transaction.atomic
def assign_commander(*, incident, commander, changed_by):
    incident.commander = commander
    incident.save(update_fields=["commander"])

    IncidentEvent.objects.create(
        incident=incident,
        user=changed_by,
        event_type=IncidentEvent.EventType.COMMANDER_ASSIGNED,
        message=f"{changed_by.email} assigned {commander.email} as commander.",
    )
    
@transaction.atomic
def change_severity(*, incident, severity, changed_by):
    old = incident.severity

    incident.severity = severity
    incident.save(update_fields=["severity"])

    IncidentEvent.objects.create(
        incident=incident,
        user=changed_by,
        event_type=IncidentEvent.EventType.SEVERITY_CHANGED,
        message=f"Severity changed from {old} to {severity}.",
    )
    
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