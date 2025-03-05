from rest_framework import serializers
from tasks.models import Task
from django.contrib.auth.models import User


class AdminTaskSerializer(serializers.ModelSerializer):
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


class UserTaskSerializer(serializers.ModelSerializer):
    opis = serializers.CharField(required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ["id", "nazwa", "opis", "status", "user"]


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task.history.model
        fields = [
            "id",
            "history_date",
            "history_type",
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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def validate_email(self, value):
        """Check if the email is aleady registerd"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use")

        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
