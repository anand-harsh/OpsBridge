from .models import Membership


def has_role(user, organization, *roles):
    return Membership.objects.filter(
        user=user,
        organization=organization,
        role__in=roles,
    ).exists()


def is_owner(user, organization):
    return has_role(user, organization, Membership.Role.OWNER)


def is_admin(user, organization):
    return has_role(
        user,
        organization,
        Membership.Role.OWNER,
        Membership.Role.ADMIN,
    )