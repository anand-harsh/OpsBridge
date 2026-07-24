from rest_framework import generics

from .models import Incident
from .serializers import IncidentSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import (
    ChangeSeveritySerializer,
    IncidentSerializer,
)
from .services import change_severity



class IncidentListCreateView(generics.ListCreateAPIView):

    serializer_class = IncidentSerializer

    def get_queryset(self):
        return (
            Incident.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "service",
                "commander",
                "created_by",
            )
            .distinct()
        )


class IncidentDetailView(generics.RetrieveAPIView):

    serializer_class = IncidentSerializer

    def get_queryset(self):
        return (
            Incident.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related(
                "organization",
                "service",
                "commander",
                "created_by",
            )
        )
        
class IncidentSeverityUpdateView(generics.GenericAPIView):

    serializer_class = ChangeSeveritySerializer

    def patch(self, request, pk):

        incident = Incident.objects.get(pk=pk)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        incident = change_severity(
            incident=incident,
            severity=serializer.validated_data["severity"],
            changed_by=request.user,
        )

        return Response(
            IncidentSerializer(incident).data,
            status=status.HTTP_200_OK,
        )