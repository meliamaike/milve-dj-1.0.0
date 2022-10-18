from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

""" class User(AbstractUser):
    class Role(models.TextCHoices):
        ADMIN = "ADMIN", 'Admin'
        CLIENT = "CLIENT", 'Client'
        GERENTE = "GERENTE", 'Gerente'
    
    base_role = Role.ADMIN

    role = models.CharField(max_length = 50, choices = Role.choices)

    def save(self, *arg, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs) """

         

class Employee(models.Model):
    name = models.CharField(max_length = 40)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Service(models.Model):
    SERVICE_CATEGORIES =(
        ('geln', 'Gel nail'),
        ('kapn', 'Kapping nail'),
        ('acrn','Acrylic nail'),
        ('lifting','Lifting lashes'),
        ('extension','Extension lashes'),
        ('perfilado','Perfilado de cejas'),
        ('threading','Threading de cejas'),
        ('facial','Tratamiento facial')
    )
    
    category = models.CharField(max_length=4, choices= SERVICE_CATEGORIES)
    duration = models.PositiveBigIntegerField()
    
    def __str__(self):
        return f'{self.category}: {self.duration} mins'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    #employee = models.ForeignKey(Employee, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.user} ha reservado {self.service} desde las {self.check_in} a las {self.check_out} .'

    def get_service_category(self):
        service_categories= dict(self.service.SERVICE_CATEGORIES)
        service_category = service_categories.get(self.service.category)
        return service_category
    
    def get_cancel_booking_url(self):
        return reverse('reservation:CancelBookingView', args=[self.pk, ])

class PaymentType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):return f'Payment option {self.name}'

class Payment(models.Model):
    payment_type_id = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(User, on_delete=CASCADE)
    staff_id = models.ForeignKey(Receptionist, on_delete=CASCADE)
    amount = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f'Cliente {self.customer_id} amount:{self.amount} processed by staff {self.staff_id}'