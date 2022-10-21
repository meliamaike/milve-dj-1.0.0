from django.contrib import admin
from .models import Service, Booking, Employee, User


# My Custom User


@admin.register(User)
class ServiceUser(admin.ModelAdmin):
    list_display = ("email", "username", "first_name", "is_active", "is_staff")
    ordering = ("-date_joined",)
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
                    "first_name",
                    "last_name",
                    "birth",
                    "celphone_number",
                    "address",
                )
            },
        ),
        (
            "Permisos",
            {
                "fields": ("is_staff", "is_active"),
            },
        ),
    )


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
    list_display = ("id", "name", "age")
    ordering = ("id",)
    list_display_links = ("name",)
    list_per_page = 5
