from rest_framework import serializers
from tasks.models import Task
from django.contrib.auth.models import User


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    # TODO: require that the user is unauthenticated to register
    class Meta:
        model = User
        fields = ["username", "password", "email"]

    # TODO: test to make sure that the email is unique
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
