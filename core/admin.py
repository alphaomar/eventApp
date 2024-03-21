from django.contrib import admin
from core.models import Event, Venue, Ticket, Organizer, EventCategory


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "start_time",
        "end_time",
        "visibility",
    ]
    list_filter = ["start_time", "end_time", "title"]


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    pass

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    pass

