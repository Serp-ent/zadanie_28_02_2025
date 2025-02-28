from tasks.models import Task
from django.contrib.auth.models import User
import os
import django

# This contains sample data for manual testing
ash = User(username="ash", email="ash@example.com", password="ash")
misty = User(username="misty", email="misty@example.com", password="misty")
brock = User(username="brock", email="brock@example.com", password="brock")
users = [
    ash,
    misty,
    brock,
    *[
        # Generic Users
        User(username=f"user{i}", password=f"user{i}")
        for i in range(5)
    ],
]
User.objects.bulk_create(users)
print("Created test users records")


tasks = [
    Task(nazwa="ash_task", opis="To jest task dla Asha", user=ash),
    Task(
        nazwa="misty_task", opis="To jest task dla mistya", user=misty, status="W_TOKU"
    ),
    Task(
        nazwa="brock_task",
        opis="To jest task dla brocka",
        user=brock,
        status="ROZWIĄZANY",
    ),
    *[
        # Unassigned tasks
        Task(nazwa=f"task{i}")
        for i in range(5)
    ],
]
Task.objects.bulk_create(tasks)
print("Created test tasks records")
