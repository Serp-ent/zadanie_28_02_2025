import pytest
from rest_framework.test import APIClient
from tasks.models import Task
from django.contrib.auth.models import User


@pytest.fixture
def anon_client():
    return APIClient()


@pytest.fixture
def user1():
    return User.objects.create_user(
        username="user1",
        password="user1",
    )


@pytest.fixture
def auth_client(user1):
    client = APIClient()
    client.force_authenticate(user1)
    return client


@pytest.fixture
def task():
    return Task.objects.create(nazwa="name")

def another_task():
    return Task.objects.create(nazwa="another_task")