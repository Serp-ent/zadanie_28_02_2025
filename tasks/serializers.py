from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    opis = serializers.CharField(required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "nazwa",
            "opis",
            "status",
            "user",
        ]


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task.history.model
        fields = [
            "id",
            "history_date",
            "nazwa",
            "opis",
            "status",
            "user",
        ]
