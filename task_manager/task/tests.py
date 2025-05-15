from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.status.models import Status
from .models import Task

class TaskCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.performer = User.objects.create_user(username='performer', password='password')
        self.status = Status.objects.create(name='In Progress')

        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            performer=self.performer,
            creator=self.user
        )

    def test_task_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('tasks_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.description)

    def test_task_create(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('tasks_create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.pk,
            'performer': self.performer.pk
        })
        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.get(name='New Task')
        self.assertEqual(new_task.creator, self.user)

    def test_task_update(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('tasks_update', args=[self.task.pk]), {
            'name': 'Updated Task',
            'description': self.task.description,
            'status': self.status.pk,
            'performer': self.performer.pk
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_by_creator(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('tasks_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertEqual(Task.objects.count(), 0)

    def test_task_delete_by_other_user_forbidden(self):
        other_user = User.objects.create_user(username='other', password='password')
        self.client.login(username='other', password='password')
        response = self.client.post(reverse('tasks_delete', args=[self.task.pk]), follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задачу может удалить только ее автор')
        self.assertEqual(Task.objects.count(), 1)
