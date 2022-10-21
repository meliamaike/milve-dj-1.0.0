from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
from django.forms import ImageField
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class Neighborhood(models.Model):
    NEIGHBORHOOD_CATEGORIES = (
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

    category = models.CharField(max_length=30, choices=NEIGHBORHOOD_CATEGORIES)


class Genre(models.Model):
    class Role(models.TextChoices):
        WOMAN = "MUJER", "Mujer"
        MAN = "HOMBRE", "Hombre"
        NA = "NO RESPONDE", "No responde"

    base_role = Role.NA

    role = models.CharField(max_length=50, choices=Role.choices)


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, username, first_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("El Superuser debe tener is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("El Superuser debe tener is_superuser=True.")

        # return self.create_user(email, username, first_name, password, **other_fields)

        s_user = self.model(
            username=username,
            first_name=first_name,
            email=email,
            **other_fields,
        )
        s_user.set_password(password)
        s_user.save()
        return s_user

    def create_user(
        self,
        username,
        first_name,
        last_name,
        email,
        password,
        celphone_number,
        address,
        birth,
        **other_fields,
    ):
        if not email:
            raise ValueError(("Debes ingresar un email"))

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            celphone_number=celphone_number,
            address=address,
            birth=birth,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):

    neighborhood = models.ForeignKey(
        Neighborhood, on_delete=models.CASCADE, blank=True, null=True
    )
    celphone_number = models.CharField(max_length=15, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="images/", null=True)
    address = models.CharField(max_length=50, blank=True)
    birth = models.DateField(blank=True, null=True)

    objects = CustomUserManager()
    REQUIRED_FIELDS = ["first_name", "email"]

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
    EMPLOYEE_CATEGORIES = (
        ("milagros", "Milagros"),
        ("mariana", "Mariana"),
        ("monica", "Monica"),
    )

    name = models.CharField(max_length=15, choices=EMPLOYEE_CATEGORIES)
    age = models.IntegerField()

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

    category = models.CharField(max_length=10, choices=SERVICE_CATEGORIES)
    duration = models.PositiveBigIntegerField()

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
            "reservation:CancelBookingView",
            args=[
                self.pk,
            ],
        )
