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

    @action(
        detail=True,
        methods=["GET"],
        url_path="history",
        url_name="history",
    )
    def task_history(self, request: Request, pk=None):
        task = self.get_object()
        queryset = task.history

        as_of = request.query_params.get("as_of")
        if as_of:
            try:
                target_date = datetime.fromisoformat(as_of)
                print("target_date=", target_date)
                historical = task.history.as_of(target_date)
                serializer = TaskHistorySerializer(historical)
                return Response(serializer.data)
            except ValueError:
                return Response(
                    {"error": "Invalid date format (e.g., 2024-01-15T12:00:00Z)"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = TaskHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="history",
        url_name="list-history",
    )
    def history(self, request: Request):
        queryset = Task.history.all().order_by("-history_date")
        serializer = TaskHistorySerializer(queryset, many=True)

        return Response(serializer.data)
