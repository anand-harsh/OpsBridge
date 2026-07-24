from apps.organizations.models import Membership


def is_org_admin(user, organization):
    return Membership.objects.filter(
        organization=organization,
        user=user,
        role__in=[
            Membership.Role.OWNER,
            Membership.Role.ADMIN,
        ],
    ).exists()