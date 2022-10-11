from django.db import models

# Create your models here.

class Service(models.Model):
    SERVICE_CATEGORIES =(
        ('GELN', 'GEL-NAIL'),
        ('KAPN', 'KAPPING-NAIL'),
        ('ACRN','ACRYLIC-NAIL'),
        ('LIFT','LIFTING-LASHES'),
        ('EXTE','THREADING-LASHES'),
        ('PERF','PERFILADO-CEJAS'),
        ('THRE','THREADING-CEJAS'),
        ('FACI','FACIAL')
    )
    
    category = models.CharField(max_length=4, choices= SERVICE_CATEGORIES)
    duration = models.FloatField()
    
    def __str__(self):
        return f'{self.category}: {self.duration} mins'

