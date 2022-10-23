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
        first_name,
        last_name,
        barrio,
        genre,
        address,
        cellphone_number,
        birth,
        password=None,
    ):
        if not email:
            raise ValueError("Debe ingresar un email.")
        if not username:
            raise ValueError("Debe ingresar un nombre de usuario.")
        if not first_name:
            raise ValueError("Debe ingresar un nombre.")
        if not last_name:
            raise ValueError("Debe ingresar un apellido.")
        if not barrio:
            raise ValueError("Debe elegir un barrio.")
        if not genre:
            raise ValueError("Debe elegir un genero.")
        if not address:
            raise ValueError("Debe ingresar una direccion.")
        if not cellphone_number:
            raise ValueError("Debe ingresar un numero de telefono.")
        if not birth:
            raise ValueError("Debe ingresar una fecha de nacimiento.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            barrio=barrio,
            genre=genre,
            address=address,
            cellphone_number=cellphone_number,
            birth=birth,
            password=password,
        )
        user.password = make_password(user.password)
        user.save()
        return user

    def create_superuser(
        self,
        email,
        username,
        first_name,
        password,
    ):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
        )
        user.password = make_password(user.password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


# Profile pic
def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "app\static\app\img\logo2.png"


class User(AbstractBaseUser, PermissionsMixin):

    """email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    barrio = models.ForeignKey(
        barrio, on_delete=models.CASCADE, blank=True, null=True
    )
    #cellphone_regex = RegexValidator(regex=r"[\d]{3}-[\d]{3}-[\d]{3}", message="Ingresa un numero valido")
    cellphone_number = models.CharField(max_length=15, blank=True)
    #cellphone_number = models.CharField(validators = [cellphone_regex],max_length=15, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=get_profile_image_filepath, null=True, default=get_default_profile_image)
    address = models.CharField(max_length=50, blank=True)
    birth = models.DateField(blank=True, null=True)"""

    class Meta:
        verbose_name = "user"

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, verbose_name="username", unique=True)
    password = models.CharField(verbose_name="password", max_length=256)
    date_joined = models.DateTimeField(verbose_name="dated_joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(verbose_name="first_name", max_length=30)
    last_name = models.CharField(max_length=20, verbose_name="last_name",blank=True)
    cellphone_number = models.CharField(
        max_length=20, verbose_name="cellphone_number",blank=True
    )
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=50, verbose_name="address", blank=True)
    birth = models.DateField(verbose_name="birth",blank=True, null=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [
        "email",
        "first_name",
    ]

    objects = CustomUserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __int__(self):
        return self.id

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_id(self):
        return self.id

    def get_profile_image_filename(self):
        return str(self.image)[str(self.image).index(f"profile_images/{self.pk}/") :]

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"
        GERENTE = "GERENTE", "Gerente"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *arg, **kwargs):
        # Si el usuario todavia no ha sido creado
        if not self.pk:
            self.role = self.base_role  # decimos que su rol es el de admin
            return super().save(*arg, **kwargs)

    def __str__(self):
        return self.username




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
    """EMPLOYEE_CATEGORIES = (
        ("milagros", "Milagros"),
        ("mariana", "Mariana"),
        ("monica", "Monica"),
    )"""

    employee = models.CharField(_("empleado"), max_length=15)
    age = models.IntegerField(_("edad"))

    def __str__(self):
        return f"{self.name}"


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
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} ha reservado {self.service} desde las {self.check_in} a las {self.check_out} ."

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
