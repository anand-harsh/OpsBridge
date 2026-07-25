from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F
from django.utils import timezone

from apps.incidents.models import Incident


def get_dashboard_summary(user):
    incidents = Incident.objects.filter(
        organization__memberships__user=user
    ).distinct()

    open_count = incidents.exclude(
        status=Incident.Status.RESOLVED
    ).count()

    critical_count = incidents.filter(
        severity=Incident.Severity.SEV1
    ).count()

    today = timezone.now().date()

    resolved_today = incidents.filter(
        resolved_at__date=today
    ).count()

    avg_resolution = incidents.filter(
        resolved_at__isnull=False
    ).annotate(
        resolution_time=ExpressionWrapper(
            F("resolved_at") - F("started_at"),
            output_field=DurationField(),
        )
    ).aggregate(
        average=Avg("resolution_time")
    )["average"]

    return {
        "open_incidents": open_count,
        "critical_incidents": critical_count,
        "resolved_today": resolved_today,
        "average_resolution_time": avg_resolution,
    }
    
def incidents_by_severity(user):
    return (
        Incident.objects.filter(
            organization__memberships__user=user
        )
        .values("severity")
        .annotate(
            count=Count("id")
        )
        .order_by("severity")
    )
    
def incidents_by_service(user):
    return (
        Incident.objects.filter(
            organization__memberships__user=user
        )
        .values("service__name")
        .annotate(
            incident_count=Count("id")
        )
        .order_by("-incident_count")
    )
    
from apps.incidents.models import IncidentEvent


def recent_activity(user):
    return (
        IncidentEvent.objects.filter(
            incident__organization__memberships__user=user
        )
        .select_related(
            "incident",
            "user",
        )
        .order_by("-created_at")[:20]
    )