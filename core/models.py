from django.db import models
from user_management import settings
from .managers import TicketManager, EventManager, VenueManager


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return self.street


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.created_at


class BaseModel(TimestampMixin):
    class Meta:
        abstract = True


class UserProfile(Address):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.last_name


class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Organizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Event(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True)
    banner_image = models.ImageField(upload_to='event_banners', blank=True, null=True)
    visibility = models.BooleanField(default=True)  # Visibility for unpublished events

    objects = EventManager()

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    sale_start_date = models.DateTimeField()
    sale_end_date = models.DateTimeField()
    description = models.TextField(blank=True)
    early_bird_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    seat_number = models.CharField(max_length=20, blank=True)
    discount_code = models.CharField(max_length=20, blank=True)

    objects = TicketManager()

    def __str__(self):
        return self.price


class Venue(Address):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    contact_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    amenities = models.TextField()
    photo = models.ImageField(upload_to='venue_photos', blank=True, null=True)
    description = models.TextField()  # Detailed venue information for attendees

    objects = VenueManager()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    event_date = models.DateField()
    duration_hours = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.venue.name


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100)
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Pending')
    booking_notes = models.TextField(blank=True, null=True)  # Notes for organizers


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
