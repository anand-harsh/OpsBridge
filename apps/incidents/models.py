from django.conf import settings
from django.db import models

from apps.organizations.models import Organization
from apps.services.models import Service


class Incident(models.Model):

    class Severity(models.TextChoices):
        SEV1 = "SEV1", "Critical"
        SEV2 = "SEV2", "High"
        SEV3 = "SEV3", "Medium"
        SEV4 = "SEV4", "Low"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        INVESTIGATING = "INVESTIGATING", "Investigating"
        MONITORING = "MONITORING", "Monitoring"
        RESOLVED = "RESOLVED", "Resolved"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="incidents",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="incidents",
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.SEV3,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    commander = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="commanded_incidents",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_incidents",
    )

    started_at = models.DateTimeField(auto_now_add=True)

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class IncidentEvent(models.Model):

    class EventType(models.TextChoices):
        CREATED = "CREATED", "Created"
        STATUS_CHANGED = "STATUS_CHANGED", "Status Changed"
        SEVERITY_CHANGED = "SEVERITY_CHANGED", "Severity Changed"
        COMMANDER_ASSIGNED = "COMMANDER_ASSIGNED", "Commander Assigned"
        COMMENT_ADDED = "COMMENT_ADDED", "Comment Added"
        RESOLVED = "RESOLVED", "Resolved"

    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name="events",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    event_type = models.CharField(
        max_length=40,
        choices=EventType.choices,
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.incident.title} - {self.event_type}"
    
class Comment(models.Model):
    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.email} - {self.incident.title}"