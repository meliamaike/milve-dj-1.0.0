from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import Service, Booking, Employee, User
from .forms import RegistrationForm


@admin.register(User)
# Si pongo UserAdmin hashea la pass, sino no.
class CustomUserAdmin(admin.ModelAdmin):
    # add_form = RegistrationForm
    list_display = (
        "email",
        "username",
        "first_name",
        "is_active",
        "is_staff",
        "is_admin",
    )
    ordering = ("date_joined",)
    list_display_links = ("username",)
    list_per_page = 15
    search_fields = (
        "email",
        "username",
        "first_name",
    )
    list_filter = ("email", "username", "first_name", "is_active", "is_staff")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "birth",
                    "cellphone_number",
                    "address",
                )
            },
        ),
        (
            "Permisos",
            {
                "fields": ("is_staff", "is_active", "is_admin"),
            },
        ),
    )


# admin.site.register(User,UserAdmin)


# Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "duration")
    ordering = ("id",)
    list_display_links = ("category",)
    list_per_page = 15


# Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    ordering = ("check_in", "check_out")
    search_fields = ("check_in", "check_out")
    list_filter = ("check_in", "check_out")
    list_per_page = 15


# Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "age")
    ordering = ("id",)
    list_display_links = ("employee",)
    list_per_page = 5
