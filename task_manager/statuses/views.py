from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Status


class StatusesIndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_index')
    success_message = 'Статус успешно создан'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = 'Статус успешно изменен'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')
    success_message = 'Статус успешно удален'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить статус, потому что он используется одной или несколькими задачами."
            )
            return redirect(self.success_url)