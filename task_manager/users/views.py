from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from .models import User
from .forms import UserCreateForm, UserUpdateForm

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = 'User created successfully! Please log in.'

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')
    success_message = 'User updated successfully!'

    def test_func(self):
        return self.get_object() == self.request.user

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')
    success_message = 'User deleted successfully!'

    def test_func(self):
        return self.get_object() == self.request.user

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = 'Logged in successfully!'

    def get_success_url(self):
        return reverse_lazy('index')

def user_logout(request):
    logout(request)
    return redirect('index')