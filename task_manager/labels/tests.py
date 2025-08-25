import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from .models import Label

User = get_user_model()


@pytest.mark.django_db
class LabelCRUDTests(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user.set_password('testpass123')
        self.user.save()
        
        self.status = Status.objects.first()

    def test_label_list_requires_login(self):
        """Test that label list requires authentication"""
        url = reverse('labels_index')
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_label_list_authenticated(self):
        """Test that authenticated user can view label list"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('labels_index')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Labels')

    def test_label_create_requires_login(self):
        """Test that label creation requires authentication"""
        url = reverse('label_create')
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_label_create_authenticated(self):
        """Test that authenticated user can create label"""
        self.client.login(username='user1', password='testpass123')
        initial_count = Label.objects.count()
        
        url = reverse('label_create')
        data = {'name': 'New Label'}
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), initial_count + 1)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("successfully" in str(msg).lower() for msg in messages))

    def test_label_create_duplicate_name(self):
        """Test that duplicate label names are not allowed"""
        Label.objects.create(name='Existing Label')
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('label_create')
        data = {'name': 'Existing Label'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')

    def test_label_update_requires_login(self):
        """Test that label update requires authentication"""
        label = Label.objects.create(name='Test Label')
        url = reverse('label_update', kwargs={'pk': label.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_label_update_authenticated(self):
        """Test that authenticated user can update label"""
        label = Label.objects.create(name='Old Name')
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('label_update', kwargs={'pk': label.pk})
        data = {'name': 'Updated Name'}
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('labels_index'))
        label.refresh_from_db()
        self.assertEqual(label.name, 'Updated Name')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("successfully" in str(msg).lower() for msg in messages))

    def test_label_delete_requires_login(self):
        """Test that label deletion requires authentication"""
        label = Label.objects.create(name='Test Label')
        url = reverse('label_delete', kwargs={'pk': label.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_label_delete_authenticated(self):
        """Test that authenticated user can delete unused label"""
        label = Label.objects.create(name='To Delete')
        self.client.login(username='user1', password='testpass123')
        initial_count = Label.objects.count()
        
        url = reverse('label_delete', kwargs={'pk': label.pk})
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), initial_count - 1)
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("successfully" in str(msg).lower() for msg in messages))

    def test_cannot_delete_label_used_by_task(self):
        """Test that label cannot be deleted if used by task"""
        label = Label.objects.create(name='Used Label')
        task = Task.objects.create(
            name='Test Task',
            status=self.status,
            author=self.user
        )
        task.labels.add(label)
        
        self.client.login(username='user1', password='testpass123')
        initial_count = Label.objects.count()
        
        url = reverse('label_delete', kwargs={'pk': label.pk})
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), initial_count)
        self.assertTrue(Label.objects.filter(pk=label.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("being used" in str(msg).lower() for msg in messages))

    def test_label_str_representation(self):
        """Test string representation of Label model"""
        label = Label.objects.create(name='Test Label')
        self.assertEqual(str(label), 'Test Label')