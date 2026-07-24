from django.urls import path

from .views import (
    IncidentDetailView,
    IncidentListCreateView,
    IncidentSeverityUpdateView,
    AssignCommanderView,
    IncidentStatusView,
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
]