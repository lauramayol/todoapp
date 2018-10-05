import datetime

from django.db import models
from django.utils import timezone


class TodoList(models.Model):
    title = models.CharField(max_length=50)
    completed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date_created = models.DateTimeField('date created')
    due_date = models.DateTimeField('due date')
    is_completed = models.BooleanField(default=False)

    def days_remaining(self):
        now = timezone.now()
        return (now - self.due_date).days

    def __str__(self):
        return self.name
