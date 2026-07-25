from django.urls import path

from .views import (
    ActivityView,
    DashboardSummaryView,
    DashboardView,
    ServiceStatsView,
    SeverityStatsView,
)

urlpatterns = [
    path("", DashboardView.as_view()),
    path("summary/", DashboardSummaryView.as_view()),
    path("severity/", SeverityStatsView.as_view()),
    path("services/", ServiceStatsView.as_view()),
    path("activity/", ActivityView.as_view()),
]