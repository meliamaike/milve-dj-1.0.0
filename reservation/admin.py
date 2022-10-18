from django.contrib import admin
from .models import Service, Booking, Employee

# Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'duration')
    ordering =('id',)
    list_display_links = ('category',)
    list_per_page = 15

#Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    ordering =('check_in','check_out')
    search_fields=('check_in','check_out')
    list_filter =('check_in','check_out')
    list_per_page = 15

#Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age')
    ordering =('id',)
    list_display_links = ('name',)
    list_per_page = 15
    