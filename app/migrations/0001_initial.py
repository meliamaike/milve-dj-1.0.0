# Generated by Django 4.1.2 on 2022-10-23 00:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0013_alter_user_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=60, unique=True, verbose_name="email"),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=30, unique=True, verbose_name="username"
                    ),
                ),
                ("password", models.CharField(max_length=256, verbose_name="password")),
                (
                    "date_joined",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="dated_joined"
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(auto_now=True, verbose_name="last_login"),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "first_name",
                    models.CharField(max_length=30, verbose_name="first_name"),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="last_name"
                    ),
                ),
                (
                    "cellphone_number",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="cellphone_number"
                    ),
                ),
                (
                    "address",
                    models.CharField(blank=True, max_length=50, verbose_name="address"),
                ),
                (
                    "birth",
                    models.DateField(blank=True, null=True, verbose_name="birth"),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("ADMIN", "Admin"),
                            ("CLIENT", "Client"),
                            ("GERENTE", "Gerente"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
            },
        ),
        migrations.CreateModel(
            name="Barrio",
            fields=[
                ("id_barrio", models.AutoField(primary_key=True, serialize=False)),
                ("barrio", models.CharField(max_length=50, verbose_name="barrio")),
                ("comuna", models.IntegerField(verbose_name="comuna")),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("employee", models.CharField(max_length=15, verbose_name="empleado")),
                ("age", models.IntegerField(verbose_name="edad")),
            ],
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id_genre", models.AutoField(primary_key=True, serialize=False)),
                ("genre", models.CharField(max_length=50, verbose_name="genero")),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category", models.CharField(max_length=50, verbose_name="categoria")),
                ("duration", models.PositiveBigIntegerField(verbose_name="duracion")),
            ],
        ),
        migrations.CreateModel(
            name="GerenteProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gerente_id", models.IntegerField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClientProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("client_id", models.IntegerField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("check_in", models.DateTimeField()),
                ("check_out", models.DateTimeField()),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.employee"
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.service"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="barrio",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.barrio",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="genre",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.genre",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.CreateModel(
            name="Client",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("app.user",),
            managers=[
                ("client", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="Gerente",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("app.user",),
            managers=[
                ("gerente", django.db.models.manager.Manager()),
            ],
        ),
    ]
