from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

class UserCreateTest(TestCase):

    def test_valid_create_user(self):
        form_data = {
            'username': 'newuser',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(reverse('users_create'), data=form_data)

        # Проверяем, что был редирект после успешной регистрации
        self.assertRedirects(response, reverse('login'))

        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username='newuser').exists())


class UserUpdateTest(TestCase):
    fixtures = ['users.json']  # Указание на файл с тестовыми данными

    def setUp(self):
        # Пользователь 1 — владелец профиля
        self.user1 = User.objects.get(pk=3)
        self.user1.set_password('123')  # Устанавливаем реальный пароль
        self.user1.save()

        # Пользователь 2 — левый юзер
        self.user2 = User.objects.create_user(
            username='hacker',
            password='password2',
            first_name='Хакер'
        )

    def test_auth_user_update_valid_data(self):

        self.client.login(username='chupakabra', password='123')  # Логинимся как валидный юзер

        url = reverse('users_update', kwargs={'pk': self.user1.pk})
        form_data = {
            'first_name': 'Игорь',
            'last_name': 'Смирнов',
            'username': 'chupakabra',  # Имя пользователя должно оставаться уникальным
            'password1': 'newpass123',
            'password2': 'newpass123',
        }

        response = self.client.post(url, data=form_data)

        # Проверяем редирект после успешного обновления
        self.assertRedirects(response, reverse('users_list'))

        # Обновляем пользователя из базы
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'Игорь')
        self.assertTrue(self.user1.check_password('newpass123'))

    def test_user_cannot_update_other_user(self):
        # Логинимся как user2 (не владелец)
        self.client.login(username='hacker', password='password2')

        # Пытаемся изменить профиль user1
        url = reverse('users_update', kwargs={'pk': self.user1.pk})
        form_data = {
            'first_name': 'Взломано',
            'last_name': 'Взломано',
            'username': 'testuser',
            'password1': 'newpass123',
            'password2': 'newpass123',
        }

        response = self.client.post(url, data=form_data)

        # Проверяем редирект или отказ
        self.assertRedirects(response, reverse('users_list'))

        # Обновляем из базы и проверяем, что имя не изменилось
        self.user1.refresh_from_db()
        self.assertNotEqual(self.user1.first_name, 'Взломано')


class UserDeleteTest(TestCase):
    fixtures = ['users.json']  # Указание на файл с тестовыми данными

    def setUp(self):
        # Пользователь 1 — владелец профиля
        self.user1 = User.objects.get(pk=3)
        self.user1.set_password('123')  # Устанавливаем реальный пароль
        self.user1.save()

        # Пользователь 2 — левый юзер
        self.user2 = User.objects.create_user(
            username='hacker',
            password='password2',
            first_name='Хакер'
        )

    def test_auth_user_delete(self):

        self.client.login(username='chupakabra', password='123')  # Логинимся как валидный юзер

        # Пытаемся удалить профиль user1
        url = reverse('users_delete', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('users_list'))

        # Проверка, что пользователь больше не существует
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())

    def test_user_cannot_delete_other_user(self):
        # Логинимся как user2 (не владелец)
        self.client.login(username='hacker', password='password2')

        # Пытаемся удалить профиль user1
        url = reverse('users_update', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('users_list'))

        # Проверка, что пользователь больше не существует
        self.assertTrue(User.objects.filter(pk=self.user1.pk).exists())
