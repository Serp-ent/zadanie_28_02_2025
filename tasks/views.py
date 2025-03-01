from django.shortcuts import render
from datetime import datetime
from tasks.models import Task
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from tasks.serializers import TaskSerializer, TaskHistorySerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from tasks.filters import TaskFilter


# Create your views here.
class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter


class TaskHistoryViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskHistorySerializer
    queryset = Task.history.all().order_by("-history_date")

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "history_date": ["gte", "lte"],
        "history_type": ["exact"],
        "id": ["exact"],
        "user": ["exact"],
        "status": ["exact"],
    }

    def get_queryset(self):
        return self.queryset.select_related("user")
