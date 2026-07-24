from django.urls import path

from .views import (
    OrganizationDetailView,
    OrganizationListCreateView,
)

urlpatterns = [
    path("", OrganizationListCreateView.as_view()),
    path("<slug:slug>/", OrganizationDetailView.as_view()),
]