from django.db import transaction
from django.utils import timezone

from .models import Incident, IncidentEvent
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Comment, IncidentEvent

VALID_TRANSITIONS = {
    Incident.Status.OPEN: [
        Incident.Status.INVESTIGATING,
    ],
    Incident.Status.INVESTIGATING: [
        Incident.Status.MONITORING,
    ],
    Incident.Status.MONITORING: [
        Incident.Status.RESOLVED,
    ],
}

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


@transaction.atomic
def assign_commander(*, incident, commander, changed_by):
    old_commander = incident.commander

    incident.commander = commander
    incident.save(update_fields=["commander"])

    IncidentEvent.objects.create(
        incident=incident,
        user=changed_by,
        event_type=IncidentEvent.EventType.COMMANDER_ASSIGNED,
        message=(
            f"Commander changed from "
            f"{old_commander.email if old_commander else 'None'} "
            f"to {commander.email}"
        ),
    )

    return incident


@transaction.atomic
def change_status(
    *,
    incident,
    status,
    changed_by,
):

    allowed = VALID_TRANSITIONS.get(
        incident.status,
        [],
    )

    if status not in allowed:
        raise ValidationError(
            f"Cannot move from {incident.status} to {status}"
        )

    incident.status = status

    if status == Incident.Status.RESOLVED:
        incident.resolved_at = timezone.now()

    incident.save()

    IncidentEvent.objects.create(
        incident=incident,
        user=changed_by,
        event_type=IncidentEvent.EventType.STATUS_CHANGED,
        message=f"Status changed to {status}",
    )

    return incident



@transaction.atomic
def add_comment(*, incident, author, body):

    comment = Comment.objects.create(
        incident=incident,
        author=author,
        body=body,
    )

    IncidentEvent.objects.create(
        incident=incident,
        user=author,
        event_type=IncidentEvent.EventType.COMMENT_ADDED,
        message=body,
    )

    return comment
