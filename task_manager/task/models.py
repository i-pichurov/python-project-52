from django.db import models
from django.contrib.auth.models import User
from task_manager.status.models import Status
from task_manager.tag.models import Tag

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    performer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_assigned',
        null=True,
        blank=True,
        default=None
        )
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(
        Tag,
        through='TaskTag',
        blank=True,
        )


class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('task', 'tag')
