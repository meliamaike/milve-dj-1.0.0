from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, password_validation
from allauth.account.forms import SignupForm, BaseSignupForm
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
    username = forms.CharField(max_length=50, label=_("Nombre de usuario"), required=True, 
    widget=forms.TextInput(
            attrs={"placeholder": _("Nombre de usuario")}
        ),)
    email = forms.EmailField(
        max_length=50,
        label=_("Correo electrónico"),
        required=True,
        widget=forms.TextInput(
            attrs={"type": "email", "placeholder": _("Correo electrónico")}
        ),
    )
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Correo electrónico*'



    def save(self, request):
        user = super(RegistrationForm, self).save(request)
        user.username = self.cleaned_data["username"]
        # user.first_name = self.cleaned_data["first_name"]
        # user.last_name = self.cleaned_data["last_name"]
        # user.cellphone_number = self.cleaned_data["cellphone_number"]
        # user.birth = self.cleaned_data["birth"]
        # user.barrio = self.cleaned_data["barrio"]
        # user.genre = self.cleaned_data["genre"]
        # user.address = self.cleaned_data["address"]
        # user.set_password(self.cleaned_data["password1"])
        user.save()
        return user


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="Nombre")
    last_name = forms.CharField(max_length=50, label="Apellido")
    email = forms.EmailField(max_length=150, label="E-mail")
    message = forms.CharField(widget=forms.Textarea, max_length=2000, label="Mensaje")


class DateInput(forms.DateInput):
    input_type = "date"


class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput, label="Fecha del turno")

    class Meta:
        model = Booking
        fields = (
            
            "service",
            "date",
            "timeslot",
        )
        labels = {
            
            "service": "Servicio",
            "timeslot": "Horario"
        }

    def clean_date(self):
        day = self.cleaned_data["date"]

        if day <= date.today():
            raise forms.ValidationError(
                "No puede elegir un día que ya pasó.", code="invalid"
            )
        if day.isoweekday() in (0, 6):
            raise forms.ValidationError(
                "Nuestro horario de trabajo es de lunes a viernes de 10:00 a 18:30 horas.",
                code="invalid",
            )

        return day


# Interactua con el modelo User para poder hacer el update de los datos. 

class UpdateUserForm(forms.ModelForm):

    birth = forms.DateField(
        label="Fecha de Nacimiento", required=False, widget=DateInput
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "cellphone_number",
            "barrio",
            "genre",
            "address",
            "birth",
        ]
