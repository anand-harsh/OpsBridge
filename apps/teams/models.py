from django.conf import settings
from django.db import models

from apps.organizations.models import Organization


class Team(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="teams",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(
        blank=True
    )

    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_teams",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ("organization", "name")

    def __str__(self):
        return f"{self.organization.name} - {self.name}"
    
class TeamMember(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_memberships",
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("team", "user")

    def __str__(self):
        return f"{self.user.email} - {self.team.name}"