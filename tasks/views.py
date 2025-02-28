from django.shortcuts import render
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework import viewsets

# Create your views here.
class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

