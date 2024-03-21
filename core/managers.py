from django.db import models
from .querysets import EventQuerySet, TicketQuerySet, VenueQuerySet


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model)

    def upcoming_events(self):
        return self.get_queryset().upcoming_events()

    def past_events(self):
        return self.get_queryset().past_events()

    def visible_events(self):
        return self.get_queryset().visible_events()

    def by_category(self, category):
        return self.get_queryset().by_category(category)

    def with_ticket_count(self):
        return self.get_queryset().with_ticket_count()

    def total_tickets_sold(self):
        return self.get_queryset().total_tickets_sold()

    def trending_events(self):
        return self.get_queryset().trending_event()


class TicketManager(models.Manager):
    def get_queryset(self):
        return TicketQuerySet(self.model)

    def available_tickets(self):
        return self.get_queryset().available_tickets()

    def early_bird_tickets(self):
        return self.get_queryset().early_bird_tickets()

    def total_quantity_sold(self):
        return self.get_queryset().total_quantity_sold()

    def upcoming_tickets(self):
        return self.get_queryset().upcoming_tickets()


class VenueManager(models.Manager):
    def get_queryset(self):
        return VenueQuerySet(self.model)

    def with_capacity(self, capacity):
        return self.get_queryset().with_capacity(capacity)

    def featured_venue(self):
        return self.get_queryset().featured_venues()
