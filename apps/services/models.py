from django.db import models

from apps.organizations.models import Organization
from apps.teams.models import Team


class Service(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="services",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="services",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_service_per_organization",
            )
        ]

    def __str__(self):
        return self.name