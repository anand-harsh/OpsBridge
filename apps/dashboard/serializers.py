from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    open_incidents = serializers.IntegerField()
    critical_incidents = serializers.IntegerField()
    resolved_today = serializers.IntegerField()
    average_resolution_time = serializers.DurationField(
        allow_null=True
    )


class SeveritySerializer(serializers.Serializer):
    severity = serializers.CharField()
    count = serializers.IntegerField()


class ServiceSerializer(serializers.Serializer):
    service__name = serializers.CharField()
    incident_count = serializers.IntegerField()


class ActivitySerializer(serializers.Serializer):
    incident = serializers.CharField(source="incident.title")
    user = serializers.CharField(source="user.email")
    event = serializers.CharField(source="event_type")
    message = serializers.CharField()
    created_at = serializers.DateTimeField()