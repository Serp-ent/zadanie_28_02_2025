from tasks.models import Task
from django.core.exceptions import ValidationError
import pytest

# TODO: test that status can be either of 3 values ("Nowy", 'W Toku', 'Rozwiązany')

# TODO: tests that default status is 'Nowy'
# TODO: tests taht Opis field inside task can be empty

# TODO: tests taht ID field of Task cannot be changed

# TODO: tests for task updating

# TODO: tests for tasks filtering

# TODO: tests for tasks history, filter for history only for given tasks, get how the tasks looked like in given time and to whom it was assigned to

# TODO: tests for user login endpoint
# TODO: tests for user register endpoint
# TODO: tests for user permissions (Admin, IsAssignedToTask)


@pytest.mark.django_db
def test_task_default_status_value():
    t = Task.objects.create(
        nazwa="name",
        opis="opis",
    )

    assert t.status == "NOWY"


@pytest.mark.django_db
@pytest.mark.parametrize("status", ["NOWY", "W_TOKU", "ROZWIĄZANY"])
def test_task_status_value_if_providen(status):
    t = Task.objects.create(
        nazwa="name",
        opis="opis",
        status=status,
    )

    assert t.status == status


@pytest.mark.django_db
@pytest.mark.parametrize("status", ["invalid1", "invalid2"])
def test_task_invalid_status_value(status):
    with pytest.raises(ValidationError) as e:
        t = Task.objects.create(
            nazwa="name",
            opis="opis",
            status=status,
        )

    assert 'invalid status' in str(e.value)
