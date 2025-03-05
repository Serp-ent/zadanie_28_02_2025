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
def other_user():
    return User.objects.create_user(
        username="other_user",
        password="other_user",
    )


@pytest.fixture
@pytest.mark.django_db
def admin():
    return User.objects.create_superuser(username="admin", password="admin")


@pytest.fixture
def auth_client(user1):
    client = APIClient()
    client.force_authenticate(user1)
    return client

@pytest.fixture
def other_auth_client(other_user):
    client = APIClient()
    client.force_authenticate(other_user)
    return client


@pytest.fixture
def admin_client(admin):
    client = APIClient()
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def task():
    return Task.objects.create(nazwa="name")


@pytest.fixture
def free_task():
    return Task.objects.create(nazwa="name")


@pytest.fixture
def another_task():
    return Task.objects.create(nazwa="another_task")


@pytest.fixture
def register_payload():
    return {
        "username": "1",
        "email": "1@example.com",
        "password": "1",
    }


@pytest.fixture
def task_payload():
    return {
        "nazwa": "taskName",
        "opis": "opis1",
        "status": "NOWY",
    }
