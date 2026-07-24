from rest_framework import serializers

from .models import Organization
from .services import create_organization


class OrganizationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "slug",
            "owner",
            "created_at",
        )

    def create(self, validated_data):
        return create_organization(
            owner=self.context["request"].user,
            **validated_data
        )