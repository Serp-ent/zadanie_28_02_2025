import pytest
from tasks.filters import TaskFilter
from django.contrib.auth.models import User
from tasks.models import Task


@pytest.mark.django_db
class TestTaskFilter:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.ash = User.objects.create_user(username="ash")
        self.misty = User.objects.create_user(username="misty")
        self.brock = User.objects.create_user(username="brock")

        # Create test tasks
        Task.objects.bulk_create(
            [
                Task(
                    nazwa="Task 1",
                    opis="Important project",
                    user=self.ash,
                    status="NOWY",
                ),
                Task(
                    nazwa="Task 2",
                    opis="Urgent bug fix",
                    user=self.misty,
                    status="W_TOKU",
                ),
                Task(
                    nazwa="Task 3",
                    opis="General maintenance",
                    user=self.brock,
                    status="ROZWIĄZANY",
                ),
                Task(
                    nazwa="Task 4",
                    opis="Important meeting",
                    user=self.ash,
                    status="W_TOKU",
                ),
                Task(
                    nazwa="Task 5",
                    opis="Critical security patch",
                    user=None,
                    status="NOWY",
                ),
            ]
        )

    @pytest.mark.parametrize(
        "filter_params,want_count",
        [
            ({"username": "ash"}, 2),
            ({"username": "s"}, 3),
            ({"username": "brock"}, 1),
            ({"username": "BOB"}, 0),
        ],
        ids=[
            "Match exactly Ash",
            "Match those containing 's' (misty + ash Tasks)",
            "Match those for brock",
            "Don't match nonexisting",
        ],
    )
    def test_filters_for_username_match(self, filter_params, want_count):
        queryset = Task.objects.all()
        filterset = TaskFilter(filter_params, queryset=queryset)

        assert filterset.is_valid()
        assert filterset.qs.count() == want_count

    @pytest.mark.parametrize(
        "filter_params,want_count",
        [
            ({"user": "ash_id"}, 2),
            ({"user": "misty_id"}, 1),
            ({"user": "brock_id"}, 1),
        ],
        ids=["ash-tasks", "misty-tasks", "brock-tasks"],
    )
    def test_filters_for_username_match(self, filter_params, want_count):
        user_id_map = {
            "ash_id": self.ash.id,
            "misty_id": self.misty.id,
            "brock_id": self.brock.id,
        }

        # Get actual id
        user_id = user_id_map.get(filter_params["user"], filter_params["user"])
        filter_params = {"user": user_id}

        queryset = Task.objects.all()
        filterset = TaskFilter(filter_params, queryset=queryset)

        assert filterset.is_valid(), filterset.errors
        assert filterset.qs.count() == want_count

    @pytest.mark.parametrize(
        "filterparams,want",
        [
            ({"status": "NOWY"}, 2),
            ({"status": "W_TOKU"}, 2),
            ({"status": "ROZWIĄZANY"}, 1),
        ],
        ids=["filter NOWY", "filter W_TOKU", "filter ROZWIĄZANY"],
    )
    def test_filters_for_status(self, filterparams, want):
        queryset = Task.objects.all()
        filterset = TaskFilter(filterparams, queryset=queryset)

        assert filterset.is_valid(), filterset.errors
        assert filterset.qs.count() == want

    @pytest.mark.parametrize(
        "filterparams, want",
        [
            ({"opis": "important"}, 2),
            ({"opis": "bug"}, 1),
            ({"opis": "CRITICAL"}, 1),  # case-insensitive
        ],
    )
    def test_filters_for_description(self, filterparams, want):
        queryset = Task.objects.all()
        filterset = TaskFilter(filterparams, queryset=queryset)

        assert filterset.is_valid(), filterset.errors
        assert filterset.qs.count() == want

    @pytest.mark.parametrize(
        "filterparams, want",
        [
            ({"username": "sh", "opis": "important"}, 2),
            ({"status": "NOWY", "opis": "project"}, 1),
        ],
    )
    def test_combined_filters(self, filterparams, want):
        queryset = Task.objects.all()
        filterset = TaskFilter(filterparams, queryset=queryset)

        assert filterset.is_valid()
        assert filterset.qs.count() == want

    @pytest.mark.parametrize('filterparams, want', [
        ({"unassigned": True}, 1),
        ({"unassigned": False}, 4),
        ({}, 5),
    ], ids=['unassigned', 'assigned', 'all'])
    def test_free_tasks(self, filterparams, want):
        queryset = Task.objects.all()
        filterset = TaskFilter(filterparams, queryset=queryset)

        assert filterset.is_valid(), filterset.errors
        assert filterset.qs.count() == want
