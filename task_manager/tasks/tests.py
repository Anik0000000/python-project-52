import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from .models import Task

User = get_user_model()


@pytest.mark.django_db
class TaskCRUDTests(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user1.set_password('testpass123')
        self.user2.set_password('testpass123')
        self.user1.save()
        self.user2.save()
        
        self.status = Status.objects.first()
        
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user1,
            executor=self.user2
        )

    def test_task_list_requires_login(self):
        """Test that task list requires authentication"""
        url = reverse('tasks_index')
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_task_list_authenticated(self):
        """Test that authenticated user can view task list"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('tasks_index')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tasks')
        self.assertContains(response, 'Test Task')

    def test_task_detail_requires_login(self):
        """Test that task detail requires authentication"""
        url = reverse('task_show', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_task_detail_authenticated(self):
        """Test that authenticated user can view task detail"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('task_show', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        self.assertContains(response, 'Test Description')

    def test_task_create_requires_login(self):
        """Test that task creation requires authentication"""
        url = reverse('task_create')
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_task_create_authenticated(self):
        """Test that authenticated user can create task"""
        self.client.login(username='user1', password='testpass123')
        initial_count = Task.objects.count()
        
        url = reverse('task_create')
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.pk,
            'executor': self.user2.pk
        }
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), initial_count + 1)
        
        new_task = Task.objects.get(name='New Task')
        self.assertEqual(new_task.author, self.user1)
        self.assertEqual(new_task.executor, self.user2)
        self.assertEqual(new_task.status, self.status)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("successfully" in str(msg).lower() for msg in messages))

    def test_task_update_requires_login(self):
        """Test that task update requires authentication"""
        url = reverse('task_update', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_task_update_authenticated(self):
        """Test that authenticated user can update task"""
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('task_update', kwargs={'pk': self.task.pk})
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.pk,
            'executor': self.user1.pk
        }
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('tasks_index'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertEqual(self.task.executor, self.user1)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("successfully" in str(msg).lower() for msg in messages))

    def test_task_delete_requires_login(self):
        """Test that task deletion requires authentication"""
        url = reverse('task_delete', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_task_delete_by_author(self):
        """Test that task author can delete task"""
        self.client.login(username='user1', password='testpass123')
        initial_count = Task.objects.count()
        
        url = reverse('task_delete', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), initial_count - 1)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("successfully" in str(msg).lower() for msg in messages))

    def test_task_delete_by_non_author(self):
        """Test that non-author cannot delete task"""
        self.client.login(username='user2', password='testpass123')
        initial_count = Task.objects.count()
        
        url = reverse('task_delete', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), initial_count)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("your own tasks" in str(msg).lower() for msg in messages))

    def test_task_str_representation(self):
        """Test string representation of Task model"""
        self.assertEqual(str(self.task), 'Test Task')

    def test_task_author_set_automatically(self):
        """Test that task author is set automatically on creation"""
        self.client.login(username='user2', password='testpass123')
        
        url = reverse('task_create')
        data = {
            'name': 'Auto Author Task',
            'description': 'Test auto author',
            'status': self.status.pk,
        }
        response = self.client.post(url, data)
        
        task = Task.objects.get(name='Auto Author Task')
        self.assertEqual(task.author, self.user2)