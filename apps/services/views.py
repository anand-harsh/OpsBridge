from rest_framework import generics

from .models import Service
from .serializers import ServiceSerializer


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return (
            Service.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "team",
            )
            .distinct()
            .order_by("name")
        )


class ServiceDetailView(generics.RetrieveAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return (
            Service.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "team",
            )
        )