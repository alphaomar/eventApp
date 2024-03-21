from django.urls import path
from .views import RegularUserRegisterView, RegisterOrganizerView, LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/user/', RegularUserRegisterView.as_view(), name='register_regular_user'),
    path('register/organizer/', RegisterOrganizerView.as_view(), name='register_organizer'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
