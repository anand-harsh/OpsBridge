from .models import Incident
from django.shortcuts import get_object_or_404

from itertools import chain

from .models import (
    IncidentEvent,
    Comment,
)



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
    

def get_incident_for_user(pk, user):
    return get_object_or_404(
        Incident.objects.select_related(
            "organization",
            "service",
            "commander",
            "created_by",
        ),
        pk=pk,
        organization__memberships__user=user,
    )


def get_incident_timeline(incident):

    events = IncidentEvent.objects.filter(
        incident=incident
    ).select_related("user")

    comments = Comment.objects.filter(
        incident=incident
    ).select_related("author")

    timeline = sorted(
        chain(events, comments),
        key=lambda x: x.created_at,
        reverse=True,
    )

    return timeline