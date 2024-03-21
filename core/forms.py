from django import forms
from django.forms.utils import ValidationError
from django.forms import TextInput
from phonenumber_field.formfields import PhoneNumberField
#from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Event, Ticket, Venue
from django.forms import DateInput


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class DatePickerInput(DateInput):
    input_type = 'date'


class PhoneNumberInput(TextInput):
    input_type = 'tel'

    def clean(self, value):
        value = super().clean(value)
        try:
            phone_number = PhoneNumberField().clean(value)
        except ValidationError as e:
            raise ValidationError(e.messages[0])
        return phone_number


class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'organizer', 'category', 'banner_image',
                  'visibility']
        labels = {
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'organizer': 'Organizer',
            'banner_image': 'Banner Image',
        }
        widgets = {
            'start_time': DateTimePickerInput(),  # Replace with your preferred widget
            'end_time': DateTimePickerInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        organizer = cleaned_data.get('organizer')
        category = cleaned_data.get('category')

        if end_time and start_time and end_time <= start_time:
            raise ValidationError("End time must be after start time")

        # if organizer and not organizer.exists():
        #     raise ValidationError("Selected organizer does not exists")
        # if category and not category.exists():
        #     raise ValidationError("Selected category does not exists")
        return cleaned_data

    def save(self, commit=True):
        event = super().save(commit=False)
        if commit:
            event.save()
        return event


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event', 'ticket_type', 'price', 'quantity_available', 'sale_start_date',
                  'sale_end_date', 'description', 'early_bird_price', 'seat_number', 'discount_code']
        labels = {
            'ticket_type': 'Ticket Type',
            'sale_start_date': "Sale Start Date",
            'sale_end_date': "Sale End Date",
            'seat_number': 'Start Number',
            'discount_code': 'Discount Code',
        }
        widgets = {
            'sale_start_date': DateTimePickerInput(),
            'sale_end_date': DateTimePickerInput(),

        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        quantity_available = cleaned_data.get('quantity_available')
        sale_start_date = cleaned_data.get('sale_start_date')
        sale_end_date = cleaned_data.get('sale_end_date')
        early_bird_price = cleaned_data.get('early_bird_price')

        if not price or price <= 0:
            raise ValidationError("Price must be a positive decimal number")

        if not quantity_available or quantity_available < 0:
            raise ValidationError("Quantity available must be a non-negative integer")

        if sale_end_date and sale_start_date and sale_end_date <= sale_start_date:
            raise ValidationError("Sale end date must be after sale start date")

        if early_bird_price is not None and early_bird_price < 0:
            raise ValidationError("Early bird price must be a non-negative decimal")

        return cleaned_data

    def save(self, commit=True):
        ticket = super().save(commit=False)
        if commit:
            ticket.save()
        return ticket


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'street', 'city', 'state', 'country', 'zip_code', 'capacity', 'contact_name', 'phone_number',
                  'amenities', 'photo', 'description']

        labels = {
            'name': 'Venue Name',
            'street': 'Street Address',
            'zip_code': 'Zip Code',
            'phone_number': 'Phone Number',
        }
        widgets = {
            'phone_number': PhoneNumberInput(),  # Replace with your preferred widget
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Validate phone number format using regex
        # Add your validation logic here
        return phone_number

