from django.urls import path

from .views import (
    IncidentCommentView,
    IncidentDetailView,
    IncidentListCreateView,
    IncidentSeverityUpdateView,
    AssignCommanderView,
    IncidentStatusView,
    IncidentTimelineView,
)

urlpatterns = [
    path("", IncidentListCreateView.as_view(), name="incident-list"),
    path("<int:pk>/", IncidentDetailView.as_view(), name="incident-detail"),
    path(
    "<int:pk>/severity/",
    IncidentSeverityUpdateView.as_view(),
),
    path(
    "<int:pk>/commander/",
    AssignCommanderView.as_view(),
),
    path(
    "<int:pk>/status/",
    IncidentStatusView.as_view(),
),
    path(
    "<int:pk>/comments/",
    IncidentCommentView.as_view(),
),
    path(
    "<int:pk>/timeline/",
    IncidentTimelineView.as_view(),
),
]