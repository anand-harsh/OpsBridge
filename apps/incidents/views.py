from rest_framework import generics

from .models import Incident
from .serializers import ChangeStatusSerializer, CommentSerializer, IncidentSerializer, TimelineSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import (
    ChangeSeveritySerializer,
    IncidentSerializer,
)
from .serializers import (
    AssignCommanderSerializer,
    IncidentSerializer,
)
from django.shortcuts import get_object_or_404
from .selectors import get_incident_for_user, list_incidents
from .services import (
    create_incident,
    change_severity,
    assign_commander,
    change_status,
)
from rest_framework.views import APIView

from .selectors import (
    get_incident_for_user,
    get_incident_timeline,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)

from .filters import IncidentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

# class IncidentListCreateView(generics.ListCreateAPIView):

#     serializer_class = IncidentSerializer

#     def get_queryset(self):
#         return (
#             Incident.objects.filter(
#                 organization__memberships__user=self.request.user
#             )
#             .select_related(
#                 "organization",
#                 "service",
#                 "commander",
#                 "created_by",
#             )
#             .distinct()
#         )

class IncidentListCreateView(generics.ListCreateAPIView):

    serializer_class = IncidentSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = IncidentFilter

    search_fields = [
        "title",
        "description",
        "service__name",
    ]

    ordering_fields = [
        "created_at",
        "severity",
        "status",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        return list_incidents(self.request.user)

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

class AssignCommanderView(generics.GenericAPIView):

    serializer_class = AssignCommanderSerializer

    def patch(self, request, pk):

        incident =get_incident_for_user(pk, request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        incident = assign_commander(
            incident=incident,
            commander=serializer.validated_data["commander"],
            changed_by=request.user,
        )

        return Response(
            IncidentSerializer(incident).data
        )
        
class IncidentStatusView(generics.GenericAPIView):

    serializer_class = ChangeStatusSerializer

    def patch(self, request, pk):

        incident = get_object_or_404(
            Incident,
            pk=pk,
            organization__memberships__user=request.user,
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        incident = change_status(
            incident=incident,
            status=serializer.validated_data["status"],
            changed_by=request.user,
        )

        return Response(
            IncidentSerializer(incident).data
        )
        
class IncidentCommentView(generics.CreateAPIView):

    serializer_class = CommentSerializer

    def get_incident(self):
        return get_incident_for_user(
            self.kwargs["pk"],
            self.request.user,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["incident"] = self.get_incident()
        return context
    



class IncidentTimelineView(APIView):

    def get(self, request, pk):

        incident = get_incident_for_user(
            pk,
            request.user,
        )

        timeline = get_incident_timeline(
            incident
        )

        serializer = TimelineSerializer(
            timeline,
            many=True,
        )

        return Response(serializer.data)