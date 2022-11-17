from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
from django.forms import ImageField
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from PIL import Image


class Barrio(models.Model):
    BARRIO_CATEGORIES = (
        ("agronomia", "AGRONOMIA (COMUNA 15)"),
        ("almagro", "ALMAGRO (COMUNA 5)"),
        ("balvanera", "BALVANERA (COMUNA 3)"),
        ("barracas", "BARRACAS (COMUNA 4)"),
        ("belgrano", "BELGRANO (COMUNA 13)"),
        ("boca", "BOCA (COMUNA 4)"),
        ("boedo", "BOEDO (COMUNA 5)"),
        ("caballito", "CABALLITO (COMUNA 6)"),
        ("chacarita", "CHACARITA (COMUNA 15)"),
        ("coghlan", "COGHLAN (COMUNA 12)"),
        ("colegiales", "COLEGIALES (COMUNA 13)"),
        ("constitucion", "CONSTITUCION (COMUNA 1)"),
        ("flores", "FLORES (COMUNA 10)"),
        ("floresta", "FLORESTA (COMUNA 10)"),
        ("liniers", "LINIERS (COMUNA 9)"),
        ("mataderos", "MATADEROS (COMUNA 9)"),
        ("monserrat", "MONTSERRAT (COMUNA 1)"),
        ("monte-castro", "MONTE CASTRO (COMUNA 10)"),
        ("nueva-pompeya", "NUEVA POMPEYA (COMUNA 4)"),
        ("nunez", "NUÑEZ (COMUNA 13)"),
        ("palermo", "PALERMO (COMUNA 14)"),
        ("parque-avellaneda", "PARQUE AVELLANEDA (COMUNA 9)"),
        ("parque-chacabuco", "PARQUE CHACABUCO (COMUNA 7)"),
        ("parque-chas", "PARQUE CHAS (COMUNA 15)"),
        ("parque-patricios", "PARQUE PATRICIOS (COMUNA 4)"),
        ("paternal", "PATERNAL (COMUNA 15)"),
        ("puerto-madero", "PUERTO MADERO (COMUNA 1)"),
        ("recoleta", "RECOLETA (COMUNA 2)"),
        ("retiro", "RETIRO(COMUNA 1)"),
        ("saavedra", "SAAVEDRA (COMUNA 12)"),
        ("san-cristobal", "SAN CRISTOBAL (COMUNA 3)"),
        ("san-nicolas", "SAN NICOLAS (COMUNA 1)"),
        ("san-telmo", "SAN TELMO (COMUNA 1)"),
        ("velez-sarfield", "VELEZ SARFIELD (COMUNA 10)"),
        ("versalles", "VERSALLES (COMUNA 10)"),
        ("villa-crespo", "VILLA CRESPO (COMUNA 15 )"),
        ("villa-del-parque", "VILLA DEL PARQUE (COMUNA 11 )"),
        ("villa-devoto", "VILLA DEVOTO (COMUNA 11 )"),
        ("villa-gral-mitre", "VILLA GRAL. MITRE (COMUNA 11 )"),
        ("villa-lugano", "VILLA LUGANO (COMUNA 8 )"),
        ("villa-luro", "VILLA LURO (COMUNA 10 )"),
        ("villa-ortuzar", "VILLA ORTUZAR (COMUNA 15 )"),
        ("villa-pueyrredon", "VILLA PUEYRREDON (COMUNA 12 )"),
        ("villa-real", "VILLA REAL (COMUNA 10 )"),
        ("villa-riachuelo", "VILLA RIACHUELO (COMUNA 8 )"),
        ("villa-santa-rita", "VILLA SANTA RITA (COMUNA 11 )"),
        ("villa-soldati", "VILLA SOLDATI (COMUNA 8)"),
        ("villa-urquiza", "VILLA URQUIZA(COMUNA 12 )"),
    )

    category = models.CharField(max_length=30, choices=BARRIO_CATEGORIES)
    
    def __str__(self):
        return {self.category} 


class Genre(models.Model):
    class Role(models.TextChoices):
        WOMAN = "MUJER", "Mujer"
        MAN = "HOMBRE", "Hombre"
        NA = "NO RESPONDE", "No responde"

    base_role = Role.NA

    role = models.CharField(max_length=50, choices=Role.choices)

    
    def __str__(self):
        return self.role


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
        user.password = make_password(user.password)
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
        user.password = make_password(user.password)  # hash password
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Profile pic
def get_profile_image_filepath(self):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "empty.png"

from django.contrib.auth.models import PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="Nombre de usuario", max_length=50, unique=True
    )
    email = models.EmailField(verbose_name="E-mail", max_length=50, unique=True)
    password = models.CharField(verbose_name="Contraseña", max_length=256)
    date_joined = models.DateTimeField(verbose_name="Fecha inicio", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="Ultimo inicio sesion", auto_now=True
    )
    is_admin = models.BooleanField(verbose_name="Es admin", default=False)
    is_active = models.BooleanField(verbose_name="Esta activo", default=True)
    is_staff = models.BooleanField(verbose_name="Es staff", default=False)
    is_superuser = models.BooleanField(verbose_name="Es superusuario", default=False)
    first_name = models.CharField(
        verbose_name="Nombre", max_length=30, blank=True, unique=False
    )
    last_name = models.CharField(
        max_length=30, verbose_name="Apellido", blank=True, unique=False
    )
    cellphone_number = models.CharField(
        max_length=20, verbose_name="Número de teléfono", blank=True, unique=False
    )
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, verbose_name="Barrio", blank=True, null=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, verbose_name="Género", blank=True, null=True
    ) 
    address = models.CharField(max_length=50, verbose_name="Dirección", blank=True)
    birth = models.DateField(verbose_name="Fecha de Nacimiento", blank=True, null=True)
    profile_image = models.ImageField(
        verbose_name="Foto de perfil",
        max_length=255,
        upload_to=get_profile_image_filepath,
        null=True,
        blank=True,
        default=get_default_profile_image,
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "email",
        "password",
    ]

    objects = CustomUserManager()


    # Metodo para guardar todo
    def save(self, *args, **kwargs):
        is_adding = self._state.adding
        super().save(*args, **kwargs)
        if is_adding:
            self.save()
            return super().save(*args, **kwargs)
        elif not self.pk:
            return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[
            str(self.profile_image).index("profile_images/" + str(self.pk) + "/") :
        ]


#Service
class Service(models.Model):
    SERVICE_CATEGORIES = (
        ("gel_nail", "Gel nail"),
        ("kapping_nail", "Kapping nail"),
        ("acrylic_nail", "Acrylic nail"),
        ("lifting", "Lifting lashes"),
        ("extension", "Extension lashes"),
        ("perfilado_cejas", "Perfilado de cejas"),
        ("threading_cejas", "Threading de cejas"),
        ("facial", "Tratamiento facial"),
    )

    category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES)
    duration = models.PositiveBigIntegerField(_("duracion"))

    def __str__(self):
        return f"{self.category}: {self.duration} mins"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, help_text="DD-MM-AAAA")

    TIMESLOT_LIST = (
        (1, "10:00 - 10:30"),
        (2, "10:30 - 11:00"),
        (3, "11:00 - 11:30"),
        (4, "11:30 - 12:00"),
        (5, "12:00 - 12:30"),
        (6, "12:30 - 13:00"),
        (7, "13:00 - 13:30"),
        (8, "13:30 - 14:00"),
        (9, "14:00 - 14:30"),
        (10, "14:30 - 15:00"),
        (11, "15:00 - 15:30"),
        (12, "15:30 - 16:00"),
        (13, "16:00 - 16:30"),
        (14, "16:30 - 17:00"),
        (15, "17:00 - 17:30"),
        (16, "17:30 - 18:00"),
        (17, "18:00 - 18:30"),
    )

    timeslot = models.IntegerField(
        null=True,
        choices=TIMESLOT_LIST,
        default="Elija el horario",
    )

    class Meta:
        unique_together = ("user", "date", "timeslot")

    def __str__(self):
        return "Fecha: {}, Servicio: {}, Horario{}-->Cliente: {}".format(
            self.date, self.service, self.get_timeslot_display(), self.user
        )

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

class Employee(models.Model):
    EMPLOYEE_CATEGORIES = (
        (1, "Milagros"),
        (2, "Carolina"),
        (3, "Monica"),
    )

    employee = models.IntegerField(null=True, choices=EMPLOYEE_CATEGORIES)
    age = models.IntegerField()

    def __str__(self):
        return {self.employee}
