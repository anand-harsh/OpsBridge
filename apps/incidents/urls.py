from django.urls import path

from .views import (
    IncidentDetailView,
    IncidentListCreateView,
    IncidentSeverityUpdateView,
)

urlpatterns = [
    path("", IncidentListCreateView.as_view(), name="incident-list"),
    path("<int:pk>/", IncidentDetailView.as_view(), name="incident-detail"),
    path(
    "<int:pk>/severity/",
    IncidentSeverityUpdateView.as_view(),
),
]