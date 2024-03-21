from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from core.models import Event, Venue, Ticket
from django.http import Http404


class HomeView(TemplateView):
    template_name = "core/home.html"

    '''
     # Trending Events: Retrieve events with high views and bookings count for the current month
        trending_events = Event.objects.filter(
            is_active=True,
            start_time__month=timezone.now().month
        ).order_by('-views', '-bookings_count')[:3]

        # Featured Venues: Retrieve venues marked as featured
        featured_venues = Venue.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('image')[:3]  # Optimize image loading

        # Upcoming Tickets: Retrieve tickets for upcoming events with active sales
        upcoming_tickets = Ticket.objects.filter(
            is_active=True,
            sale_start_date__gte=timezone.now(),
            event__is_active=True
        ).select_related('event').order_by('sale_start_date')[:3]

        # Additional context for user engagement, personalization, and social integration
        # Example:
        # context['search_form'] = SearchForm()
        # context['user_interests'] = self.request.user.interests.all()
        # context['social_share_links'] = get_social_share_links()
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trendings_events = Event.objects.trending_events()

        featured_venues = Venue.objects.featured_venue()

        upcoming_tickets = Ticket.objects.upcoming_tickets()

        context['trending_events'] = trendings_events
        context['featured_venues'] = featured_venues
        context['upcoming_tickets'] = upcoming_tickets

        return context


class SearchEventView(ListView):
    model = Event
    template_name = "core/search_event.html"
    context_object_name = "events"

    def get_queryset(self):
        query_title = self.request.GET.get("title", "")
        query_description = self.request.GET.get("description", "")
        query_organizer = self.request.GET.get("organizer", "")
        query_category = self.request.GET.get("category")

        queryset = self.model.objects.filter(
            title__icontains=query_title,
            description__icontains=query_description,
        )

        if query_organizer:
            queryset = queryset.filter(organizer__name__icontains=query_organizer)

        if query_category:
            query_category = queryset.filter(category__name__icontains=query_category)
        return queryset


class EventListView(ListView):
    model = Event
    template_name = "core/events.html"
    context_object_name = "events"
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.all()

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['total_events'] = self.model.objects.filter(visibility=True).count()


class EventDetailView(DetailView):
    model = Event
    template_name = "core/event_detail.html"
    context_object_name = "event"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj:
            raise Http404("Events does not exists")
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
