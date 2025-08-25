import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task

User = get_user_model()


@pytest.mark.django_db
class TaskCRUDTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user1.set_password('testpass123')
        self.user2.set_password('testpass123')
        self.user1.save()
        self.user2.save()
        
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        
        self.task1 = Task.objects.create(
            name='Test Task 1',
            description='Test Description 1',
            status=self.status1,
            author=self.user1,
            executor=self.user2
        )
        self.task1.labels.add(self.label1)
        
        self.task2 = Task.objects.create(
            name='Test Task 2',
            description='Test Description 2',
            status=self.status2,
            author=self.user2,
            executor=self.user1
        )
        self.task2.labels.add(self.label2)

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
        url = reverse('task_show', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_task_detail_authenticated(self):
        """Test that authenticated user can view task detail"""
        self.client.login(username='user1', password='testpass123')
        url = reverse('task_show', kwargs={'pk': self.task1.pk})
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
            'status': self.status1.pk,
            'executor': self.user2.pk
        }
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), initial_count + 1)
        
        new_task = Task.objects.get(name='New Task')
        self.assertEqual(new_task.author, self.user1)
        self.assertEqual(new_task.executor, self.user2)
        self.assertEqual(new_task.status, self.status1)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("successfully" in str(msg).lower() for msg in messages)
        )

    def test_task_update_requires_login(self):
        """Test that task update requires authentication"""
        url = reverse('task_update', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_task_update_authenticated(self):
        """Test that authenticated user can update task"""
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('task_update', kwargs={'pk': self.task1.pk})
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status1.pk,
            'executor': self.user1.pk
        }
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('tasks_index'))
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, 'Updated Task')
        self.assertEqual(self.task1.description, 'Updated Description')
        self.assertEqual(self.task1.executor, self.user1)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("successfully" in str(msg).lower() for msg in messages)
        )

    def test_task_delete_requires_login(self):
        """Test that task deletion requires authentication"""
        url = reverse('task_delete', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        
        login_url = reverse('login')
        expected_redirect = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect)

    def test_task_delete_by_author(self):
        """Test that task author can delete task"""
        self.client.login(username='user1', password='testpass123')
        initial_count = Task.objects.count()
        
        url = reverse('task_delete', kwargs={'pk': self.task1.pk})
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), initial_count - 1)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("successfully" in str(msg).lower() for msg in messages)
        )

    def test_task_delete_by_non_author(self):
        """Test that non-author cannot delete task"""
        self.client.login(username='user2', password='testpass123')
        initial_count = Task.objects.count()
        
        url = reverse('task_delete', kwargs={'pk': self.task1.pk})
        response = self.client.post(url)
        
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(Task.objects.count(), initial_count)
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("your own tasks" in str(msg).lower() for msg in messages)
        )

    def test_task_str_representation(self):
        """Test string representation of Task model"""
        self.assertEqual(str(self.task1), 'Test Task 1')

    def test_task_author_set_automatically(self):
        """Test that task author is set automatically on creation"""
        self.client.login(username='user2', password='testpass123')
        
        url = reverse('task_create')
        data = {
            'name': 'Auto Author Task',
            'description': 'Test auto author',
            'status': self.status1.pk,
        }
        self.client.post(url, data)
        
        task = Task.objects.get(name='Auto Author Task')
        self.assertEqual(task.author, self.user2)

    # Filter Tests
    def test_filter_by_status(self):
        """Test filtering tasks by status"""
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('tasks_index')
        response = self.client.get(url, {'status': self.status1.pk})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertNotContains(response, 'Test Task 2')

    def test_filter_by_executor(self):
        """Test filtering tasks by executor"""
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('tasks_index')
        response = self.client.get(url, {'executor': self.user2.pk})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertNotContains(response, 'Test Task 2')

    def test_filter_by_labels(self):
        """Test filtering tasks by labels"""
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('tasks_index')
        response = self.client.get(url, {'labels': self.label1.pk})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertNotContains(response, 'Test Task 2')

    def test_filter_self_tasks(self):
        """Test filtering for user's own tasks"""
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('tasks_index')
        response = self.client.get(url, {'self_tasks': 'on'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertNotContains(response, 'Test Task 2')

    def test_filter_combination(self):
        """Test filtering with multiple criteria"""
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('tasks_index')
        response = self.client.get(url, {
            'status': self.status1.pk,
            'executor': self.user2.pk,
            'self_tasks': 'on'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertNotContains(response, 'Test Task 2')

    def test_no_filters_shows_all_tasks(self):
        """Test that no filters shows all tasks"""
        self.client.login(username='user1', password='testpass123')
        
        url = reverse('tasks_index')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Test Task 2')