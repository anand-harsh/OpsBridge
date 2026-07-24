from .models import Membership, Organization


def create_organization(*, owner, name):
    organization = Organization.objects.create(
        name=name,
        owner=owner,
    )

    Membership.objects.create(
        organization=organization,
        user=owner,
        role=Membership.Role.OWNER,
    )

    return organization