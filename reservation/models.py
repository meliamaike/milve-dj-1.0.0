from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length = 40)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Service(models.Model):
    SERVICE_CATEGORIES =(
        ('GELN', 'GEL-NAIL'),
        ('KAPN', 'KAPPING-NAIL'),
        ('ACRN','ACRYLIC-NAIL'),
        ('LIFT','LIFTING-LASHES'),
        ('EXTE','EXTENSION-LASHES'),
        ('PERF','PERFILADO-CEJAS'),
        ('THRE','THREADING-CEJAS'),
        ('FACI','FACIAL')
    )
    
    category = models.CharField(max_length=4, choices= SERVICE_CATEGORIES)
    duration = models.FloatField()
    
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
