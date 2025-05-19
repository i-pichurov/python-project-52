from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.tag.models import Tag
from task_manager.status.models import Status
from task_manager.task.models import Task

class TagCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tag = Tag.objects.create(name='urgent')
        self.status = Status.objects.create(name='new')

    def login(self):
        self.client.login(username='testuser', password='password')

    def test_tag_list_requires_login(self):
        response = self.client.get(reverse('tags_list'))
        self.assertRedirects(response, reverse('login'))

    def test_tag_list_view(self):
        self.login()
        response = self.client.get(reverse('tags_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tag.name)

    def test_tag_create_view(self):
        self.login()
        response = self.client.post(reverse('tags_create'), {'name': 'bug'})
        self.assertRedirects(response, reverse('tags_list'))
        self.assertTrue(Tag.objects.filter(name='bug').exists())

    def test_tag_update_view(self):
        self.login()
        response = self.client.post(reverse('tags_update', args=[self.tag.pk]), {'name': 'feature'})
        self.assertRedirects(response, reverse('tags_list'))
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'feature')

    def test_tag_delete_view(self):
        self.login()
        response = self.client.post(reverse('tags_delete', args=[self.tag.pk]))
        self.assertRedirects(response, reverse('tags_list'))
        self.assertFalse(Tag.objects.filter(pk=self.tag.pk).exists())

    def test_tag_delete_protected(self):
        self.login()
        task = Task.objects.create(
            name='Task with tag',
            description='desc',
            status=self.status,
            creator=self.user
        )
        task.tags.add(self.tag)

        response = self.client.post(reverse('tags_delete', args=[self.tag.pk]), follow=True)
        self.assertRedirects(response, reverse('tags_list'))
        self.assertTrue(Tag.objects.filter(pk=self.tag.pk).exists())
        self.assertContains(response, 'Невозможно удалить тег')
