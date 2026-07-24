from rest_framework import generics

from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return (
            Organization.objects
            .filter(memberships__user=self.request.user)
            .distinct()
        )
        
class OrganizationDetailView(generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Organization.objects
            .filter(memberships__user=self.request.user)
            .distinct()
        )