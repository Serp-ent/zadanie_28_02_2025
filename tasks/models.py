from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    TASK_STATE = [
        ("NOWY", "Nowy"),
        ("W_TOKU", "W toku"),
        ("ROZWIĄZANY", "Rozwiązany"),
    ]

    nazwa = models.CharField(max_length=100)
    opis = models.TextField()
    status = models.CharField(choices=TASK_STATE, max_length=10, default="NOWY")

    # Task does not need to have user assigned
    user = models.ForeignKey(
        User,
        related_name="tasks",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.status not in [state[0] for state in Task.TASK_STATE]:
            raise ValidationError("invalid status value")

        return super().save(*args, **kwargs)
