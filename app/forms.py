from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, password_validation
from allauth.account.forms import SignupForm,BaseSignupForm
import datetime
from app import models as UserModel
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from .models import Booking
from datetime import date


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%d %H:%M"])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%d %H:%M"])


class RegistrationForm(SignupForm):
    username = forms.CharField(max_length=50, label = "Nombre de usuario", required = True)
    email = forms.EmailField(max_length=50, label="E-mail", required=True)
    password1 = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    ) 
    password2 = forms.CharField(
        label=_("Confirma tu contraseña"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Ingrese de vuelta la contraseña."),
    )

    class Meta:
        model = get_user_model
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    
    def save(self, request):
        user = super(RegistrationForm, self).save(request)
        user.username = self.cleaned_data["username"]
        #user.first_name = self.cleaned_data["first_name"]
        #user.last_name = self.cleaned_data["last_name"]
        #user.cellphone_number = self.cleaned_data["cellphone_number"]
        #user.birth = self.cleaned_data["birth"]
        #user.barrio = self.cleaned_data["barrio"]
        #user.genre = self.cleaned_data["genre"]
        #user.address = self.cleaned_data["address"]
        # user.set_password(self.cleaned_data["password1"])
        user.save()
        return user

class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)
    

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Booking
        fields = ( 'user','service','employee','date','timeslot',)


    def clean_date(self):
        day = self.cleaned_data['date']

        if day <= date.today():
            raise forms.ValidationError('Date should be upcoming (tomorrow or later)', code='invalid')
        if day.isoweekday() in (0, 6):
            raise forms.ValidationError('Date should be a workday', code='invalid')

        return day