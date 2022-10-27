from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django import utils


class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.username = data["username"]
        user.email = data["email"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.cellphone_number = data["cellphone_number"]
        user.birth = data["birth"]
        user.barrio = data["barrio"]
        user.genre = data["genre"]
        user.address = data["address"]
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        user.save()
        return user