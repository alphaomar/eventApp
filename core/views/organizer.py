from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from account.forms import OrganizerRegistrationForm
from core.decorators import user_is_regular, user_is_organizer
from core.forms import EventCreationForm
from core.models import Event, Venue, Ticket


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_organizer, name='dispatch')
class DashboardView(ListView):
    model = Event
    template_name = "core/organizer/dashboard.html"
    context_object_name = "events"

    def get_queryset(self):
        return self.model.objects.filter(organizer=self.request.user.organizer)


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_organizer, name='dispatch')
class EventCreateView(CreateView):
    model = Event
    form_class = EventCreationForm
    template_name = "core/organizer/event_create.html"
    success_url = reverse_lazy('organizer-dashboard')

    def form_valid(self, form):
        form.instance.organizer = self.request.user.organizer
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add custom handling for invalid form submission if needed
        messages.error(self.request, "Failed to create the event. Please check the form.")
        return super().form_invalid(form)
