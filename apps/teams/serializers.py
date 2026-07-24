from rest_framework import serializers

from .models import Team, TeamMember
from .services import create_team


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = (
            "id",
            "organization",
            "name",
            "description",
            "lead",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        return create_team(**validated_data)


class TeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamMember
        fields = "__all__"