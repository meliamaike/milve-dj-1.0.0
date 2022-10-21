from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(required=True, input_formats=["%m/%d/%Y %H:%M"])
    check_out = forms.DateTimeField(required=True, input_formats=["%m/%d/%Y %H:%M"])


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        #model = User
        fields = ("username", "email", "password1", "password2")
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
