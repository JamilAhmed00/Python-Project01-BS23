from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    task_name = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    details = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_name} -> {self.assigned_to.username}"
