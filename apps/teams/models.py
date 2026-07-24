from django.conf import settings
from django.db import models

from apps.organizations.models import Organization


class Team(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="teams",
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_teams",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_team_name_per_organization",
            )
        ]

    def __str__(self):
        return self.name


class TeamMember(models.Model):

    class Role(models.TextChoices):
        LEAD = "LEAD", "Lead"
        ENGINEER = "ENGINEER", "Engineer"
        VIEWER = "VIEWER", "Viewer"

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

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ENGINEER,
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "user"],
                name="unique_user_per_team",
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.team.name}"