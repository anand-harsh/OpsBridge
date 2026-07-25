from rest_framework.permissions import BasePermission

from apps.organizations.models import Membership


class CanCreateIncident(BasePermission):

    def has_permission(self, request, view):

        organization_id = request.data.get("organization")

        if not organization_id:
            return False

        membership = Membership.objects.filter(
            organization_id=organization_id,
            user=request.user,
        ).first()

        if not membership:
            return False

        return membership.role in (
            Membership.Role.OWNER,
            Membership.Role.ADMIN,
            Membership.Role.ENGINEER,
        )