from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Profile, Event

class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255)
    security_question = forms.CharField(max_length=255)
    security_answer = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'security_question', 'security_answer']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Remove or modify the help text
        self.fields['username'].help_text = "Username should contain only letters"
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isalpha():
            raise ValidationError(_('Username should only contain letters.'), code='invalid_username')
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        profile = Profile.objects.create(
            user=user,
            phone_number=self.cleaned_data['phone_number'],
            address=self.cleaned_data['address'],
            security_question=self.cleaned_data['security_question'],
        )
        profile.set_security_answer(self.cleaned_data['security_answer'])
        profile.save()

        return user

class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        )
    )
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']

class LoginForm(AuthenticationForm):
    pass
