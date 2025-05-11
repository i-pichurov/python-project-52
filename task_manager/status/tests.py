from django.test import TestCase
from .models import Status
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.

class BaseTestCase(TestCase):
    fixtures = [
        'task_manager/user/fixtures/users.json',
        'task_manager/status/fixtures/statuses.json']


class StatusIndexTest(BaseTestCase):

    def setUp(self):
        # Пользователь 1
        self.user1 = User.objects.get(pk=3)
        self.user1.set_password('123')  # Устанавливаем реальный пароль
        self.user1.save()

    def test_auth_statuses_list(self):
        self.client.login(username='chupakabra', password='123')  # Логинимся как валидный юзер
        response = self.client.get(reverse("statuses_list"))
        # Проверяем, что страницу нам отдали
        self.assertEqual(response.status_code, 200)

    def test_not_auth_statuses_list(self):
        response = self.client.get(reverse("statuses_list"))
        # Проверяем, что был редирект на окно авторизации
        self.assertRedirects(response, reverse('login'))


class StatusCreateTest(BaseTestCase):

    def setUp(self):
        # Пользователь 1
        self.user1 = User.objects.get(pk=3)
        self.user1.set_password('123')  # Устанавливаем реальный пароль
        self.user1.save()

    def test_auth_create_status(self): # Проверяем создание статуса для авторизованного пользователя

        self.client.login(username='chupakabra', password='123')  # Логинимся как валидный юзер

        form_data = {
            'name': 'newstatus123',
        }
        response = self.client.post(reverse('statuses_create'), data=form_data)

        # Проверяем, что был редирект после успешного создания статуса
        self.assertRedirects(response, reverse('statuses_list'))

        # Проверяем, что статус создан
        self.assertTrue(Status.objects.filter(name='newstatus123').exists())

    def test_not_auth_create_status(self):

        # Пытаемся создать статус без авторизации
        form_data = {
            'name': 'newstatus123',
        }

        response = self.client.post(reverse('statuses_create'), data=form_data)

        # Проверяем редирект или отказ
        self.assertRedirects(response, reverse('login'))

        # Проверяем, что статус не создан
        self.assertFalse(Status.objects.filter(name='newstatus123').exists())


class StatusUpdateTest(BaseTestCase):

    def setUp(self):
        # Пользователь 1
        self.user1 = User.objects.get(pk=3)
        self.user1.set_password('123')  # Устанавливаем реальный пароль
        self.user1.save()

        # Статус 1
        self.status1 = Status.objects.get(pk=4)
        self.status1.save()

    def test_auth_update_status(self): # Проверяем обновление статуса для авторизованного пользователя

        self.client.login(username='chupakabra', password='123')  # Логинимся как валидный юзер

        # Пытаемся изменить статус
        url = reverse('statuses_update', kwargs={'pk': self.status1.pk})
        form_data = {
            'name': 'newstatus123',
        }
        response = self.client.post(url, data=form_data)

        # Проверяем, что был редирект после успешного обновления статуса
        self.assertRedirects(response, reverse('statuses_list'))

        # Обновляем из базы и проверяем, что статус изменился
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, 'newstatus123')

    def test_not_auth_update_status(self):

        # Пытаемся изменить статус без авторизации
        url = reverse('statuses_update', kwargs={'pk': self.status1.pk})
        form_data = {
            'name': 'newstatus123',
        }
        response = self.client.post(url, data=form_data)

        # Проверяем редирект
        self.assertRedirects(response, reverse('login'))

        # Обновляем из базы и проверяем, что статус не изменился
        self.status1.refresh_from_db()
        self.assertNotEqual(self.status1.name, 'newstatus123')


class StatusDeleteTest(BaseTestCase):

    def setUp(self):
        # Пользователь 1
        self.user1 = User.objects.get(pk=3)
        self.user1.set_password('123')  # Устанавливаем реальный пароль
        self.user1.save()

        # Статус 1
        self.status1 = Status.objects.get(pk=4)
        self.status1.save()

    def test_auth_delete_status(self): # Проверяем обновление статуса для авторизованного пользователя

        self.client.login(username='chupakabra', password='123')  # Логинимся как валидный юзер

        # Пытаемся удалить статус
        url = reverse('statuses_delete', kwargs={'pk': self.status1.pk})
        response = self.client.post(url)

        # Проверяем, что был редирект после успешного удаления статуса
        self.assertRedirects(response, reverse('statuses_list'))

        # Проверка, что статус больше не существует
        self.assertFalse(Status.objects.filter(pk=self.status1.pk).exists())

    def test_not_auth_delete_status(self):

        # Пытаемся удалить статус без авторизации
        url = reverse('statuses_delete', kwargs={'pk': self.status1.pk})
        response = self.client.post(url)

        # Проверяем редирект
        self.assertRedirects(response, reverse('login'))

        # Проверяем, что статус существует
        self.assertTrue(Status.objects.filter(pk=self.status1.pk).exists())
