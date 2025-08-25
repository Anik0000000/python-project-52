from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task

User = get_user_model()


class TasksIndexView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter for author's own tasks if checkbox is checked
        if self.request.GET.get('self_tasks'):
            queryset = queryset.filter(author=self.request.user)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Задача успешно изменена'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class TaskDeleteView(
    LoginRequiredMixin, 
    UserPassesTestMixin, 
    SuccessMessageMixin, 
    DeleteView
):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Задача успешно удалена'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                "Вы не авторизованы! Пожалуйста, выполните вход."
            )
            return super(LoginRequiredMixin, self).handle_no_permission()
        
        messages.error(
            self.request,
            "Задачу может удалить только ее автор."
        )
        return redirect('tasks_index')
