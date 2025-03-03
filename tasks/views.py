from django.shortcuts import render
from datetime import datetime
from rest_framework import mixins
from tasks.models import Task
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from tasks.serializers import (
    TaskSerializer,
    TaskHistorySerializer,
    UserSerializer,
    UserRegisterSerializer,
)
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from tasks.filters import TaskFilter, TaskHistoryFilter


# Create your views here.
class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_object(self):
        instance = super().get_object()
        as_of_value = self.request.query_params.get("as_of")
        if as_of_value:
            hisorical_instance = instance.history.as_of(as_of_value)
            return hisorical_instance

        return instance


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


class UserViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
