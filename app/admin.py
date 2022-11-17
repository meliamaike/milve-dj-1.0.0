from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import Service, Booking, User, Employee, Barrio, Genre


class CustomUserAdmin(UserAdmin):
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
    list_filter = ("email", "first_name", "is_active", "is_staff")

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
                    "profile_image",
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

admin.site.register(User,CustomUserAdmin)

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
    ordering = ("user", "service", "date", "timeslot")
    search_fields = ("date", "timeslot")
    list_filter = ("date", "timeslot")
    list_per_page = 15


# Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "age")
    ordering = ("id",)
    list_display_links = ("employee",)
    list_per_page = 5

@admin.register(Barrio)
class BarrioAdmin(admin.ModelAdmin):
    list_display = ("id", "category")
    ordering = ("id",)
    list_display_links = ("category",)
    list_per_page = 15

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "role")
    ordering = ("id",)
    list_display_links = ("role",)
    list_per_page = 15