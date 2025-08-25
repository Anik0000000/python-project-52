from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelsIndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Метка успешно создана'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Метка успешно изменена'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Метка успешно удалена'

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        return super().handle_no_permission()

    def post(self, request, *args, **kwargs):
        label_to_delete = self.get_object()
        
        # Check if label is used by any tasks
        if label_to_delete.tasks.exists():
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется "
                "одной или несколькими задачами."
            )
            return redirect(self.success_url)
            
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется "
                "одной или несколькими задачами."
            )
            return redirect(self.success_url)