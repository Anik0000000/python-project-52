from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserCRUDTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)

        for user in [self.user1, self.user2, self.user3]:
            user.set_password('testpass123')
            user.save()

    def test_user_registration(self):
        initial_users = User.objects.count()

        url = reverse('user_create')
        data = {
            'username': 'newuser',
            'password1': 'newpass123',  # NOSONAR
            'password2': 'newpass123',  # NOSONAR
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), initial_users + 1)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("успешно" in str(msg).lower() for msg in messages))

    def test_user_update_authenticated(self):
        self.client.login(username='user1', password='testpass123')  # NOSONAR
        url = reverse('user_update', kwargs={'pk': self.user1.pk})
        response = self.client.post(
            url,
            {
                'username': 'user1',  # NOSONAR
                'first_name': 'Updated',  # NOSONAR
                'last_name': 'User',  # NOSONAR
            }
        )
        self.assertRedirects(response, reverse('users_index'))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'Updated')

    def test_user_update_unauthenticated(self):
        url = reverse('user_update', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)

        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                "не авторизованы" in str(msg).lower() or 
                "not logged in" in str(msg).lower() 
                for msg in messages
            )
        )

    def test_user_delete_authenticated(self):
        self.client.login(username='user1', password='testpass123')  # NOSONAR
        initial_count = User.objects.count()
        
        url = reverse('user_delete', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('users_index'))
        self.assertEqual(User.objects.count(), initial_count - 1)
        self.assertFalse(User.objects.filter(pk=self.user1.pk).exists())

    def test_user_login(self):
        url = reverse('login')
        data = {
            'username': 'user1',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_logout(self):
        self.client.login(username='user1', password='testpass123')  # NOSONAR
        
        url = reverse('logout')
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('index'))

    def test_users_list_accessible_without_authentication(self):
        url = reverse('users_index')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пользователи')