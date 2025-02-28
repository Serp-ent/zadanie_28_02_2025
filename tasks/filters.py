import django_filters
from tasks.models import Task


# TODO: tests
class TaskFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="user__username",
        lookup_expr="icontains",
    )
    opis = django_filters.CharFilter(
        field_name="opis",
        lookup_expr="icontains",
    )

    class Meta:
        model = Task
        fields = ["user", "status", "username", "opis"]
