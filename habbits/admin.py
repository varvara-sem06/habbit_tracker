from django.contrib import admin

from .models import Habbit


@admin.register(Habbit)
class HabbitAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "owner",
        "place",
        "time",
        "is_pleasant",
        "periodicity",
        "is_public",
    )
