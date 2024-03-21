from django import forms
from account.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class RegularUserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(RegularUserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        self.fields["first_name"].widget.attrs.update({'placeholder': "Enter first name"})
        self.fields["last_name"].widget.attrs.update({'placeholder': "Enter last name"})
        self.fields["email"].widget.attrs.update({'placeholder': "Enter Email"})
        self.fields["password1"].widget.attrs.update({'placeholder': "Enter password"})
        self.fields["password2"].widget.attrs.update({'placeholder': "Confirm password"})

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        },
        error_messages = {
            "first_name": {"required": "First name is required", "max_length": "Name is too long"},
            "last_name": {"required": "Last name is required", "max_length": "Last Name is too long"},
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password2 != password1:
            self.add_error('password2', 'Password does not match')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.USER
        if commit:
            user.save()
        return user


class OrganizerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(OrganizerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"

        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Enter Last Name"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]
        # widgets = {
        #     'password1': forms.PasswordInput(),
        #     'password2': forms.PasswordInput(),
        # }
        error_messages = {
            "first_name": {"required": "First name is required", "max_length": "Name is too long"},
            "last_name": {"required": "Last name is required", "max_length": "Last Name is too long"},
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password2 != password1:
            self.add_error('password2', "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.ORGANIZER
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={
            'placeholder': 'Enter Email'
        }
    ))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            'placeholder': "Enter password"
        }
    ))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError('Invalid email or password')
            if not self.user.is_active:
                raise forms.ValidationError('This account is inactive')
            if not self.user.check_password(password):
                raise forms.ValidationError("Invalid email or password")
        return cleaned_data

    def get_user(self):
        return self.user


class RegularUserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegularUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"placeholder": "Enter First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Enter Last Name"})

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "gender"]


class OrganizerProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrganizerProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Company name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Company address"
        self.fields["first_name"].label = "Company name"
        self.fields["last_name"].label = "Company address"

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]
