import django_filters
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="user__username",
        lookup_expr="icontains",
    )
    nazwa = django_filters.CharFilter(
        field_name="nazwa",
        lookup_expr="icontains",
    )
    opis = django_filters.CharFilter(
        field_name="opis",
        lookup_expr="icontains",
    )

    unassigned = django_filters.BooleanFilter(
        method="filter_free_tasks",
        label="Are free (Without user assigned)",
    )

    class Meta:
        model = Task
        fields = ["id", "user", "status", "nazwa", "username", "opis"]

    def filter_free_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(user__isnull=True)

        return queryset.filter(user__isnull=False)


class TaskHistoryFilter(django_filters.FilterSet):
    class Meta:
        model = Task.history.model
        fields = {
            "history_date": ["gte", "lte"],
            "id": ["exact"],
            "user": ["exact"],
            "status": ["exact"],
        }
