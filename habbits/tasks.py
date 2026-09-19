from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Habbit
from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)

    habbits = Habbit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        owner__telegram_chat_id__isnull=False,
    ).exclude(owner__telegram_chat_id="")

    sent_count = 0

    for habbit in habbits:
        if habbit.last_reminded_at:
            last_reminded = timezone.localtime(habbit.last_reminded_at)

            next_reminder = last_reminded + timedelta(days=habbit.periodicity)

            if now < next_reminder:
                continue

        message = (
            "Напоминание о привычке!\n\n"
            f"Место: {habbit.place}\n"
            f"Время: {habbit.time.strftime('%H:%M')}\n"
            f"Действие: {habbit.action}"
        )

        send_telegram_message(
            habbit.owner.telegram_chat_id,
            message,
        )

        habbit.last_reminded_at = now
        habbit.save(update_fields=["last_reminded_at"])

        sent_count += 1

    return f"Отправлено напоминаний: {sent_count}"
