from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView
from .forms import RegularUserRegistrationForm, OrganizerRegistrationForm, UserLoginForm
from .models import CustomUser


# Create your views here.


class RegularUserRegisterView(CreateView):
    model = CustomUser
    form_class = RegularUserRegistrationForm
    template_name = "account/regular_user/user_register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        self.object.set_password(password)
        self.object.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.success_url)
        return super().dispatch(request, *args, **kwargs)


class RegisterOrganizerView(CreateView):
    model = CustomUser
    form_class = OrganizerRegistrationForm
    template_name = 'account/organizer/organizer.html'
    success_url = reverse_lazy('home')

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     password = form.cleaned_data.get("password1")
    #     self.object.set_password(password)
    #     self.object.save(password)
    #     return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.success_url)
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')
    extra_context = {"title": "register"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """

    url = reverse_lazy("home")  # Assuming "accounts:login" is the name of the login page URL

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "You are now logged out")
        return super().get(request, *args, **kwargs)
