from rest_framework import generics

from .models import Team
from .serializers import TeamSerializer


class TeamListCreateView(generics.ListCreateAPIView):

    serializer_class = TeamSerializer

    def get_queryset(self):
        return (
            Team.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "lead",
            )
            .distinct()
            .order_by("name")
        )


class TeamDetailView(generics.RetrieveAPIView):

    serializer_class = TeamSerializer

    def get_queryset(self):
        return (
            Team.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "lead",
            )
        )