from django.urls import reverse
import pytest
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task


# TODO: tests for tasks history, filter for history only for given tasks, get how the tasks looked like in given time and to whom it was assigned to

# TODO: tests for user permissions (Admin, IsAssignedToTask)

# TODO: admin have full access thus, he can assign task to user, or remove from user
# TODO: user can pick any free task
# TODO: only user that the task is assigned to can abandon task
# TODO: only user that the task is assigned to can edit the task


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["auth_client", "anon_client"],
    indirect=True,
)
def test_anyone_can_create_tasks_with_every_field(client):
    url = reverse("task-list")
    task_count = Task.objects.count()

    response = client.post(
        url,
        data={
            "nazwa": "taskName",
            "opis": "opis1",
            "status": "NOWY",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert task_count + 1 == Task.objects.count()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        {"opis": "opis"},
        {"status": "W_TOKU"},
        {},
    ],
    ids=["Only Opis", "Only Status", "Empty payload"],
)
def test_fail_task_creation_without_name(anon_client, payload):
    url = reverse("task-list")
    count = Task.objects.count()

    response = anon_client.post(url, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert count == Task.objects.count(), "The task objects count changed"


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["name1", "name2"])
def test_create_task_with_only_name(anon_client, name):
    url = reverse("task-list")
    count = Task.objects.count()

    response = anon_client.post(url, {"nazwa": name})

    responseJson = response.json()
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert Task.objects.count() == count + 1, "Task creation didn't add new one"
    assert responseJson["nazwa"] == name
    assert responseJson["opis"] == ""


@pytest.mark.django_db
def test_task_status_is_new_if_not_provided(anon_client):
    url = reverse("task-list")
    count = Task.objects.count()

    response = anon_client.post(
        url,
        {
            "nazwa": "name",
        },
    )

    responseJson = response.json()
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert Task.objects.count() == count + 1, "Task creation didn't add new one"
    assert responseJson["status"] == "NOWY"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "task_status,should_create",
    [
        ("NOWY", True),
        ("W_TOKU", True),
        ("ROZWIĄZANY", True),
        ("INVALID1", False),
        ("INVALID2", False),
    ],
    ids=["NEW", "RUNNING", "FINISHED", "invalid_1", "invalid_2"],
)
def test_task_status_on_creation(anon_client, task_status, should_create):
    url = reverse("task-list")
    count = Task.objects.count()

    response = anon_client.post(
        url,
        {
            "nazwa": "name",
            "status": task_status,
        },
    )

    responseJson = response.json()

    if should_create:
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        assert Task.objects.count() == count + 1, "Task creation didn't add new one"
        assert responseJson["status"] == task_status
    else:
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
        assert Task.objects.count() == count, "Failed create still creates new Task"


@pytest.mark.django_db
def test_task_id_cannot_be_updated_in_partial_update(task, anon_client):
    id = task.id
    url = reverse("task-detail", kwargs={"pk": task.id})

    new_id = task.id + 1
    response = anon_client.patch(url, {"id": new_id})

    task.refresh_from_db()

    assert task.id == id, "id was changed after update"


@pytest.mark.django_db
def test_task_id_cannot_be_updated_in_full_update(task, anon_client):
    id = task.id
    url = reverse("task-detail", kwargs={"pk": task.id})

    # Make sure it is different
    payload = {
        id: task.id + 1,
        "nazwa": f"{task.nazwa}_new",
        "opis": f"{task.opis}_new",
        "status": Task.TASK_STATE[1][0],
    }
    response = anon_client.patch(url, payload)

    task.refresh_from_db()
    assert task.id == id, "id was changed after update"
    assert task.nazwa == payload["nazwa"], "nazwa field was not updated in put"
    assert task.opis == payload["opis"], "opis field was not updated in put"
    assert task.status == payload["status"], "status field was not updated in put"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field,value",
    [
        ("nazwa", "new_name"),
        ("opis", "new_description"),
        ("status", "W_TOKU"),
    ],
)
def test_task_partial_update(anon_client, field, value):
    task = Task.objects.create(nazwa="name")
    url = reverse("task-detail", kwargs={"pk": task.id})

    response = anon_client.patch(url, {field: value})
    responseJson = response.json()

    task.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert responseJson[field] == value
    assert (
        getattr(task, field) == value
    ), f"Field '{field}' was not updated with value '{value}'"


@pytest.mark.django_db
def test_task_partial_update_with_user(anon_client, user1):
    task = Task.objects.create(nazwa="name")
    url = reverse("task-detail", kwargs={"pk": task.id})

    response = anon_client.patch(url, {"user": user1.id})
    responseJson = response.json()

    task.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert responseJson["user"] == user1.id
    assert task.user == user1


@pytest.mark.django_db
@pytest.mark.parametrize("task_status", ["invalid1", "invalid2"])
def test_partial_task_update_with_invalid_status(anon_client, task, task_status):
    task = Task.objects.create(nazwa="name")
    status_before = task.status
    url = reverse("task-detail", kwargs={"pk": task.id})

    response = anon_client.patch(url, {"status": task_status})
    responseJson = response.json()

    task.refresh_from_db()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert any("not a valid" in msg for msg in responseJson["status"])
    assert (
        task.status == status_before
    ), "task status was changed after invalid partial update status"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "update_data",
    [
        {
            "nazwa": "updated_name",
            "opis": "updated_description",
            "status": "W_TOKU",
        },
        {
            "nazwa": "updated_name",
            "opis": "updated_description",
            "status": "W_TOKU",
        },
    ],
)
def test_task_full_update(anon_client, task, update_data):
    url = reverse("task-detail", kwargs={"pk": task.id})

    response = anon_client.put(url, data=update_data)

    response_json = response.json()
    task.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert response_json["nazwa"] == update_data["nazwa"]
    assert response_json["opis"] == update_data["opis"]
    assert response_json["status"] == update_data["status"]

    assert task.nazwa == update_data["nazwa"]
    assert task.opis == update_data["opis"]
    assert task.status == update_data["status"]


@pytest.mark.django_db
def test_task_full_update_missing_required_fields(anon_client, task):
    url = reverse("task-detail", kwargs={"pk": task.id})
    invalid_data = {
        # Missing required nazwa field
        "opis": "new_description",
        "status": "W_TOKU",
    }

    response = anon_client.put(url, data=invalid_data)
    response_json = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "nazwa" in response_json


@pytest.mark.django_db
def test_task_full_update_invalid_status(anon_client, task):
    url = reverse("task-detail", kwargs={"pk": task.id})
    invalid_data = {
        "nazwa": "valid_name",
        "opis": "valid_description",
        "status": "INVALID_STATUS",
    }

    response = anon_client.put(url, data=invalid_data)
    response_json = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "status" in response_json


@pytest.mark.django_db
@pytest.mark.parametrize("task", ["task", "another_task"], indirect=True)
def test_task_detailed_view(task, anon_client):
    url = reverse("task-detail", kwargs={"pk": task.id})

    response = anon_client = anon_client.get(url)
    responseJson = response.json()

    assert (
        response.status_code == status.HTTP_200_OK
    ), "Invalid resposne from the server"
    assert responseJson["id"] == task.id
    assert responseJson["nazwa"] == task.nazwa
    assert responseJson["opis"] == task.opis
    assert responseJson["status"] == task.status
    assert responseJson["user"] == task.user


@pytest.mark.django_db
def test_task_delete_endpoint(task, anon_client):
    url = reverse("task-detail", kwargs={"pk": task.id})
    ntask_before = Task.objects.count()

    response = anon_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ntask_before - 1 == Task.objects.count(), response.json()
    assert not Task.objects.filter(pk=task.id).exists()


@pytest.mark.django_db
def test_retrieving_user():
    # TODO
    pass


@pytest.mark.django_db
def test_list_users():
    # TODO
    pass


@pytest.mark.django_db
def test_user_can_update_own_profile():
    # TODO
    pass


@pytest.mark.django_db
def test_user_cannot_update_own_profile():
    # TODO
    pass


@pytest.mark.django_db
def test_admin_can_update_any_profile():
    # TODO
    pass


@pytest.mark.django_db
@pytest.mark.parametrize('method, want', [
    ('post', status.HTTP_201_CREATED),
    ('get', status.HTTP_405_METHOD_NOT_ALLOWED),
    ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
    ('patch', status.HTTP_405_METHOD_NOT_ALLOWED),
    ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
])
def test_can_only_post_to_register(anon_client, register_payload, method, want):
    url = reverse("register")

    method = getattr(anon_client, method)
    response = method(
        url,
        data=register_payload,
    )

    assert response.status_code == want


@pytest.mark.django_db
def test_register_endpoint(anon_client, register_payload):
    url = reverse("register")

    response = anon_client.post(
        url,
        data=register_payload,
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_user_cannot_be_authenticated_to_register(auth_client, register_payload):
    url = reverse('register')
    response = auth_client.post(url, data=register_payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN, 'Authenticated users cannot register a new account'



@pytest.mark.django_db
def test_email_should_be_unique(anon_client, register_payload):
    url = reverse('register')
    User.objects.create_user(**register_payload)
    register_payload['username'] = f'{register_payload['username']}_new' # usernames are unique by default

    response = anon_client.post(url, register_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, "user emails should be unique"

@pytest.mark.django_db
def test_login_endpoint_is_available(anon_client, user1):
    """rest framework provides login endpoints just test if its connected"""
    response = anon_client.post('/api/login/', data={'username': user1.username, 'password': user1.password})

    assert response.status_code == status.HTTP_200_OK