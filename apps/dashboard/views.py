from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import (
    get_dashboard_summary,
    incidents_by_service,
    incidents_by_severity,
    recent_activity,
)
from .serializers import (
    ActivitySerializer,
    DashboardSummarySerializer,
    ServiceSerializer,
    SeveritySerializer,
)


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_dashboard_summary(request.user)
        return Response(DashboardSummarySerializer(data).data)


class SeverityStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = incidents_by_severity(request.user)
        return Response(
            SeveritySerializer(data, many=True).data
        )


class ServiceStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = incidents_by_service(request.user)
        return Response(
            ServiceSerializer(data, many=True).data
        )


class ActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = recent_activity(request.user)
        return Response(
            ActivitySerializer(data, many=True).data
        )
        
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "summary": DashboardSummarySerializer(
                get_dashboard_summary(request.user)
            ).data,
            "severity_distribution": SeveritySerializer(
                incidents_by_severity(request.user),
                many=True,
            ).data,
            "service_statistics": ServiceSerializer(
                incidents_by_service(request.user),
                many=True,
            ).data,
            "recent_activity": ActivitySerializer(
                recent_activity(request.user),
                many=True,
            ).data,
        }

        return Response(data)