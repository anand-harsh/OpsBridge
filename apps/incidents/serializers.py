from rest_framework import serializers

from .models import Incident
from .services import create_incident


class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = (
            "id",
            "service",
            "title",
            "description",
            "severity",
            "status",
            "commander",
            "created_by",
            "started_at",
            "resolved_at",
        )

        read_only_fields = (
            "status",
            "commander",
            "created_by",
            "started_at",
            "resolved_at",
        )

    def create(self, validated_data):
        return create_incident(
            user=self.context["request"].user,
            **validated_data,
        )
        
class ChangeSeveritySerializer(serializers.Serializer):
    severity = serializers.ChoiceField(
        choices=Incident.Severity.choices
    )