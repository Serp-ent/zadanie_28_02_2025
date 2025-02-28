from django.shortcuts import render
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from tasks.filters import TaskFilter

# Create your views here.
class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

