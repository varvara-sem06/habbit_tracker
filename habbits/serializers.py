from rest_framework import serializers

from .models import Habbit


class HabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habbit
        fields = "__all__"
        read_only_fields = ("owner", "last_reminded_at")

    def validate(self, attrs):
        is_pleasant = attrs.get(
            "is_pleasant",
            self.instance.is_pleasant if self.instance else False,
        )

        related_habbit = attrs.get(
            "related_habbit",
            self.instance.related_habbit if self.instance else None,
        )

        reward = attrs.get(
            "reward",
            self.instance.reward if self.instance else None,
        )

        periodicity = attrs.get(
            "periodicity",
            self.instance.periodicity if self.instance else 1,
        )

        execution_time = attrs.get(
            "execution_time",
            self.instance.execution_time if self.instance else None,
        )

        if is_pleasant and (reward or related_habbit):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь награду или связанную привычку."
            )

        if not is_pleasant and not reward and not related_habbit:
            raise serializers.ValidationError(
                "Полезная привычка должна иметь вознаграждение или связанную привычку."
            )

        if reward and related_habbit:
            raise serializers.ValidationError(
                "Нельзя одновременно указать вознаграждение и связанную привычку."
            )

        if related_habbit and not related_habbit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        if self.instance and related_habbit == self.instance:
            raise serializers.ValidationError("Нельзя связать привычку с самой собой.")

        if related_habbit:
            owner = (
                self.instance.owner if self.instance else self.context["request"].user
            )

            if related_habbit.owner != owner:
                raise serializers.ValidationError(
                    "Связанная привычка должна принадлежать тому же пользователю."
                )

        if not 1 <= periodicity <= 7:
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )

        if execution_time is not None and execution_time > 120:
            raise serializers.ValidationError(
                "Время выполнения не может превышать 120 секунд."
            )

        return attrs
