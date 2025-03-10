from django.shortcuts import render
from datetime import datetime
from rest_framework.exceptions import NotFound
from rest_framework import permissions
from rest_framework import mixins
from tasks.models import Task
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from tasks.serializers import (
    AdminTaskSerializer,
    UserTaskSerializer,
    TaskHistorySerializer,
    UserSerializer,
    UserRegisterSerializer,
)
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from tasks.filters import TaskFilter, TaskHistoryFilter
from tasks.permissions import (
    IsNotAuthenticated,
    IsOwnerOrAdmin,
    IsAdminOrReadOnly,
    IsAdminOrAssignedUser,
)


# Create your views here.
class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = AdminTaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminTaskSerializer
        return UserTaskSerializer

    def get_permissions(self):
        permissions_classes = []

        if self.action in ["list", "retrieve"]:
            permissions_classes = [permissions.AllowAny]
        elif self.action in ["partial_update", "update"]:
            permissions_classes = [IsAdminOrAssignedUser]
        elif self.action == "destroy":
            permissions_classes = [permissions.IsAdminUser]
        elif self.action == "create":
            permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

        return [permission() for permission in permissions_classes]

    def get_object(self):
        instance = super().get_object()

        as_of_value = self.request.query_params.get("as_of")
        if as_of_value:
            try:
                hisorical_instance = instance.history.as_of(as_of_value)
                return hisorical_instance
            except ValueError as e:
                raise ValidationError({"as_of": str(e)})
            except Exception as e:
                raise NotFound("No historical record found.")

        return instance

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            task_user = serializer.validated_data.get("user", user)
        else:
            task_user = user
        serializer.save(user=task_user)


class TaskHistoryViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskHistorySerializer
    queryset = Task.history.all().order_by("-history_date")

    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskHistoryFilter

    def get_queryset(self):
        return self.queryset.select_related("user")


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsNotAuthenticated]


class UserViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permissions_classes = []
        if self.action in ["list", "retrieve"]:
            permissions_classes = [permissions.AllowAny]
        else:
            permissions_classes = [IsOwnerOrAdmin]

        return [permission() for permission in permissions_classes]
