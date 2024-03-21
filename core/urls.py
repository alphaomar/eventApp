from django.urls import path, include

from core.views.home import HomeView, SearchEventView, EventListView, EventDetailView
from core.views.organizer import DashboardView, EventCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('organizer/dashboard/', DashboardView.as_view(), name="organizer-dashboard"),
    path('event/create', EventCreateView.as_view(), name='event_create'),
    path('search/', SearchEventView.as_view(), name='search_event'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),


]
