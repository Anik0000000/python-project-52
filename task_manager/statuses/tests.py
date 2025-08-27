from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Status

User = get_user_model()


class StatusCRUDTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password('testpass123')
        self.user.save()

    def test_status_list_requires_login(self):
        """Test that status list requires authentication"""
        url = reverse('statuses_index')
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_status_list_authenticated(self):
        """Test that authenticated user can view status list"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('statuses_index')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Статусы')

    def test_status_create_requires_login(self):
        """Test that status creation requires authentication"""
        url = reverse('status_create')
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_status_create_authenticated(self):
        """Test that authenticated user can create status"""
        self.client.login(username='user1', password='testpass123')
        initial_count = Status.objects.count()
        
        url = reverse('status_create')
        data = {'name': 'New Status'}
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), initial_count + 1)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

        # Status created successfully - functionality is working

    def test_status_create_duplicate_name(self):
        """Test that duplicate status names are not allowed"""
        Status.objects.create(name='Existing Status')
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('status_create')
        data = {'name': 'Existing Status'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')

    def test_status_update_requires_login(self):
        """Test that status update requires authentication"""
        status = Status.objects.create(name='Test Status')
        url = reverse('status_update', kwargs={'pk': status.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_status_update_authenticated(self):
        """Test that authenticated user can update status"""
        status = Status.objects.create(name='Old Name')
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('status_update', kwargs={'pk': status.pk})
        data = {'name': 'Updated Name'}
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('statuses_index'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated Name')

        # Status updated successfully - functionality is working

    def test_status_delete_requires_login(self):
        """Test that status deletion requires authentication"""
        status = Status.objects.create(name='Test Status')
        url = reverse('status_delete', kwargs={'pk': status.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_status_delete_authenticated(self):
        """Test that authenticated user can delete status"""
        status = Status.objects.create(name='To Delete')
        self.client.login(username='user1', password='testpass123')
        initial_count = Status.objects.count()
        
        url = reverse('status_delete', kwargs={'pk': status.pk})
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertEqual(Status.objects.count(), initial_count - 1)
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())

        # Status deleted successfully - functionality is working

    def test_status_str_representation(self):
        """Test string representation of Status model"""
        status = Status.objects.create(name='Test Status')
        self.assertEqual(str(status), 'Test Status')