from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
from django.forms import ImageField
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class Barrio(models.Model):
    id_barrio = models.AutoField(primary_key=True)
    barrio = models.CharField(_("barrio"), max_length=50, null=False)
    comuna = models.IntegerField(_("comuna"), null=False)

    def __str__(self):
        return f"{self.barrio} - COMUNA {self.comuna}"


class Genre(models.Model):
    """class Role(models.TextChoices):
        WOMAN = "MUJER", "Mujer"
        MAN = "HOMBRE", "Hombre"
        NA = "NO RESPONDE", "No responde"

    base_role = Role.NA

    role = models.CharField(max_length=50, choices=Role.choices)"""

    id_genre = models.AutoField(primary_key=True)
    genre = models.CharField(_("genero"), max_length=50)

    def __str__(self):
        return self.genre


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        password=None,
    ):
        if not email:
            raise ValueError("Debe ingresar un email.")
        if not username:
            raise ValueError("Debe ingresar un nombre de usuario.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        username,
        password,
    ):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.password = make_password(user.password) #hash password
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Profile pic
def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "app\static\app\img\logo2.png"


class User(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length = 50, unique=True)
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)
    password = models.CharField(verbose_name="password", max_length=256)
    date_joined = models.DateTimeField(verbose_name="dated_joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name="first_name", max_length=30,blank=True,unique=False)
    last_name = models.CharField(max_length=20, verbose_name="last_name", blank=True,unique=False)
    cellphone_number = models.CharField(
        max_length=20, verbose_name="cellphone_number", blank=True,unique=False
    )
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=50, verbose_name="address", blank=True)
    birth = models.DateField(verbose_name="birth", blank=True, null=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "email",
        "password",
    ]

    objects = CustomUserManager()

    #Para saber que roles tienen
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"
        GERENTE = "GERENTE", "Gerente"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        is_adding = self._state.adding
        super( ).save(*args, **kwargs)
        if is_adding:
            self.save()
            return super().save(*args, **kwargs)
        elif not self.pk:
            self.role = self.base_role  # decimos que su rol es el de admin
            return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
	    return True


class ClientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CLIENT)


class Client(User):
    base_role = User.Role.CLIENT

    client = ClientManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Solo para clientes"


@receiver(post_save, sender=Client)
def create_user_profile(sender, instance, created, **kwargs):
    # Si ha sido creado vamos a ver si su rol es de CLIENT
    if created and instance.role == "CLIENT":
        ClientProfile.objects.create(user=instance)


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.IntegerField(null=True, blank=True)


class GerenteManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.GERENTE)


class Gerente(User):
    base_role = User.Role.GERENTE

    gerente = GerenteManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Solo para gerentes"


@receiver(post_save, sender=Gerente)
def create_user_profile(sender, instance, created, **kwargs):
    # Si ha sido creado vamos a ver si su rol es de CLIENT
    if created and instance.role == "GERENTE":
        GerenteProfile.objects.create(user=instance)


class GerenteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gerente_id = models.IntegerField(null=True, blank=True)


class Employee(models.Model):
    employee = models.CharField(_("empleado"), max_length=15)
    age = models.IntegerField(_("edad"))

    def __str__(self):
        return f"{self.employee}"


class Service(models.Model):
    SERVICE_CATEGORIES = (
        ("geln", "Gel nail"),
        ("kapn", "Kapping nail"),
        ("acrn", "Acrylic nail"),
        ("lifting", "Lifting lashes"),
        ("extension", "Extension lashes"),
        ("perfilado", "Perfilado de cejas"),
        ("threading", "Threading de cejas"),
        ("facial", "Tratamiento facial"),
    )

    """ category = models.CharField(max_length=10, choices=SERVICE_CATEGORIES) """
    category = models.CharField(_("categoria"), max_length=50)
    duration = models.PositiveBigIntegerField(_("duracion"))

    def __str__(self):
        return f"{self.category}: {self.duration} mins"



class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now,help_text="AAAA-MM-DD")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    TIMESLOT_LIST = (
        ("A", '10:00 - 10:30'),
        ("B", '10:30 - 11:00'),
        ("C", '11:00 - 11:30'),
        ("D", '11:30 - 12:00'),
        ("E", '12:00 - 12:30'),
        ("F", '12:30 - 13:00'),
        ("G", '13:00 - 13:30'),
        ("H", '13:30 - 14:00'),
        ("I", '14:00 - 14:30'),
        ("J", '14:30 - 15:00'),
        ("K", '15:00 - 15:30'),
        ("L", '15:30 - 16:00'),
        ("M", '16:00 - 16:30'),
        ("N", '16:30 - 17:00'),
        ("O", '17:00 - 17:30'),
        ("P", '17:30 - 18:00'),
        ("Q", '18:00 - 18:30'),
    )

    timeslot = models.CharField(max_length=10,blank=True, null=True, choices=TIMESLOT_LIST, default="Elija el horario")
    
    class Meta:
        unique_together = ('user','date', 'timeslot','employee')
    

    def __str__(self):
        return '{} {} {} {}. Cliente: {}'.format(self.date, self.service, self.timeslot, self.employee, self.user)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]



    def get_service_category(self):
        service_categories = dict(self.service.SERVICE_CATEGORIES)
        service_category = service_categories.get(self.service.category)
        return service_category

    def get_cancel_booking_url(self):
        return reverse(
            "app:CancelBookingView",
            args=[
                self.pk,
            ],
        )
