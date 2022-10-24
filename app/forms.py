from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, password_validation
from allauth.account.forms import SignupForm
import datetime
from app import models as UserModel
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%d %H:%M"])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%d %H:%M"])


class RegistrationForm(SignupForm):
    username = forms.CharField(max_length=20, label="Nombre de usuario", required=True)
    email = forms.EmailField(max_length=50, label="Email", required=True)
    first_name = forms.CharField(max_length=50, label="Nombre", required=True)
    last_name = forms.CharField(max_length=50, label="Apellido", required=True)
    cellphone_number = forms.CharField(
        max_length=20, label="Numero de telefono", required=True
    )
    birth = forms.DateField(
        label="Birthday",
        required=False,
        initial=datetime.date.today,
        widget=forms.DateInput(
            attrs={"class": "form-control", "id": "example-date-input", "type": "date"}
        ),
    )
    barrio = forms.ModelChoiceField(
        queryset=UserModel.Barrio.objects.all(),
        empty_label="Elegi un barrio...",
        required=True,
        label="Barrio",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    genre = forms.ModelChoiceField(
        queryset=UserModel.Genre.objects.all(),
        empty_label="Elegi tu genero...",
        label="Genre",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    address = forms.CharField(max_length=50, label="Direccion", required=False)
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
            "first_name",
            "last_name",
            "cellphone_number",
            "birth",
            "barrio",
            "genre",
            "address",
            "password1",
            "password2",
        )

    def save(self, request):
        user = super(RegistrationForm, self).save(request)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.cellphone_number = self.cleaned_data["cellphone_number"]
        user.birth = self.cleaned_data["birth"]
        user.barrio = self.cleaned_data["barrio"]
        user.genre = self.cleaned_data["genre"]
        user.address = self.cleaned_data["address"]
        # user.set_password(self.cleaned_data["password1"])
        user.save()
        return user
