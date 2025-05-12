from django.db import models
from django.contrib.auth.models import User
from task_manager.status.models import Status

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tasks_assigned')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)
    # tags = models.ManyToManyField(Tag)