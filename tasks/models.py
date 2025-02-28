from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    TASK_STATE = {
        "NOWY": "Nowy",
        "W_TOKU": "W toku",
        "ROZWIĄZANY": "Rozwiązany",
    }

    nazwa = models.CharField(max_length=100)
    opis = models.TextField()
    status = models.CharField(choices=TASK_STATE, max_length=10, default=)

    # Task does not need to have user assigned
    user = models.ForeignKey(
        User,
        related_name="tasks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
