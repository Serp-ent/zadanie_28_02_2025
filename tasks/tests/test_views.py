from django.urls import reverse
import pytest
from rest_framework import status
from tasks.models import Task


# TODO: tests for tasks filtering

# TODO: tests for tasks history, filter for history only for given tasks, get how the tasks looked like in given time and to whom it was assigned to

# TODO: tests for user login endpoint
# TODO: tests for user register endpoint
# TODO: tests for user permissions (Admin, IsAssignedToTask)


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
        'nazwa': f'{task.nazwa}_new',
        'opis': f'{task.opis}_new',
        'status': Task.TASK_STATE[1][0],
    }
    response = anon_client.patch(url, payload)

    task.refresh_from_db()
    assert task.id == id, "id was changed after update"
    assert task.nazwa == payload['nazwa'], "nazwa field was not updated in put"
    assert task.opis == payload['opis'], "opis field was not updated in put"
    assert task.status == payload['status'], "status field was not updated in put"



@pytest.mark.django_db
def test_task_partial_update(task):
    # TODO
    pass

@pytest.mark.django_db
def test_task_full_update(task):
    # TODO:
    pass


@pytest.mark.django_db
@pytest.mark.parametrize('task', ['task', 'another_task'], indirect=True)
def test_task_detailed_view(task, anon_client):
    url = reverse('task-detail', kwargs={'pk': task.id})

    response = anon_client = anon_client.get(url)
    responseJson = response.json()

    assert response.status_code == status.HTTP_200_OK, "Invalid resposne from the server"
    assert responseJson['id'] == task.id
    assert responseJson['nazwa'] == task.nazwa
    assert responseJson['opis'] == task.opis
    assert responseJson['status'] == task.status
    assert responseJson['user'] == task.user


@pytest.mark.django_db
def test_task_delete_endpoint(task, anon_client):
    url = reverse('task-detail', kwargs={'pk': task.id})
    ntask_before = Task.objects.count()

    response = anon_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ntask_before - 1 == Task.objects.count(), response.json()
    assert not Task.objects.filter(pk=task.id).exists()