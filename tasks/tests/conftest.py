import pytest
from rest_framework.test import APIClient
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
