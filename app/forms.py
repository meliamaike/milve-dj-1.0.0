from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, password_validation
from allauth.account.forms import SignupForm
import datetime
from app import models as UserModel


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%d %H:%M"])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%d %H:%M"])


class RegistrationForm(SignupForm):
    first_name = forms.CharField(max_length=20, label="first_name")
    last_name = forms.CharField(max_length=20, label="last_name")
    cellphone_number = forms.CharField(max_length=20, label="cellphone_number")
    birth = forms.DateField(
        label="birth",
        initial=datetime.date.today,
        widget=forms.DateInput(
            attrs={"class": "form-control", "id": "example-date-input", "type": "date"}
        ),
    )
    barrio = forms.ModelChoiceField(
        queryset=UserModel.Barrio.objects.all(),
        empty_label=None,
        label="Grad",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    genre = forms.ModelChoiceField(
        queryset=UserModel.Genre.objects.all(),
        empty_label=None,
        label="Grad",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    address = forms.CharField(max_length=50, label="address")

    def save(self, request):
        user = super(RegistrationForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.cellphone_number = self.cleaned_data["cellphone_number"]
        user.birth = self.cleaned_data["birth"]
        user.barrio = self.cleaned_data["barrio"]
        user.genre = self.cleaned_data["genre"]
        user.address = self.cleaned_data["address"]
        user.save()
        return user


