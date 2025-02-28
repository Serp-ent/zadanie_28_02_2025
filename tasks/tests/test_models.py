from tasks.models import Task
from django.core.exceptions import ValidationError
import pytest

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
