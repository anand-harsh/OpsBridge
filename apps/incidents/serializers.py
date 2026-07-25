from rest_framework import serializers

from .models import (
    Incident,
    Comment,
    IncidentEvent,
)
from .services import (
    create_incident,
    change_severity,
    assign_commander,
    change_status,
    add_comment,
)
from django.contrib.auth import get_user_model

User = get_user_model()


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

class AssignCommanderSerializer(serializers.Serializer):
    commander = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    
class ChangeStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=Incident.Status.choices
    )
    
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "id",
            "body",
            "author",
            "created_at",
        )

        read_only_fields = (
            "author",
            "created_at",
        )

    def create(self, validated_data):

        return add_comment(
            incident=self.context["incident"],
            author=self.context["request"].user,
            body=validated_data["body"],
        )
        
class TimelineSerializer(serializers.Serializer):

    def to_representation(self, obj):

        if isinstance(obj, IncidentEvent):

            return {
                "type": "EVENT",
                "event": obj.event_type,
                "message": obj.message,
                "user": obj.user.email if obj.user else None,
                "created_at": obj.created_at,
            }

        return {
            "type": "COMMENT",
            "message": obj.body,
            "user": obj.author.email,
            "created_at": obj.created_at,
        }