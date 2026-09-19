from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Habbit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habbits",
    )

    place = models.CharField(max_length=255)

    time = models.TimeField()

    action = models.CharField(max_length=255)

    is_pleasant = models.BooleanField(default=False)

    related_habbit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=-True,
        blank=True,
        related_name="pleasant_for",
    )

    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(7),
        ],
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    execution_time = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
    )

    is_public = models.BooleanField(default=False)

    last_reminded_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.action
