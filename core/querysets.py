from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone


class EventQuerySet(models.QuerySet):
    def upcoming_events(self):
        return self.filter(start_time__gte=timezone.now())

    def past_events(self):
        return self.filter(start_time__lt=timezone.now())

    def visible_events(self):
        return self.filter(visibility=True)

    def by_category(self, category):
        return self.filter(category__name=category)

    def with_ticket_count(self):
        return self.annotate(ticket_count=Count('ticket'))

    def total_tickets_sold(self):
        return self.aggregate(total_tickets_sold=Sum('ticket__quantity_sold'))

    def trending_event(self):
        # return self.filter(start_time__month=timezone.now().month).order_by('-start_time')[:3]
        return self.all()


class TicketQuerySet(models.QuerySet):
    def available_tickets(self):
        return self.filter(quantity_available__gt=0)

    def early_bird_tickets(self):
        return self.filter(early_bird_price__isnull=False)

    def total_quantity_sold(self):
        return self.aggregate(total_quantity_sold=Sum('quantity_sold'))

    def upcoming_tickets(self):
        return self.filter(sale_start_date__gte=timezone.now()).order_by('sale_start_date')[:3]


class VenueQuerySet(models.QuerySet):
    def with_capacity(self, capacity):
        return self.filter(capacity__gte=capacity)

    def featured_venues(self):
        return self.order_by('-id')[:3]

