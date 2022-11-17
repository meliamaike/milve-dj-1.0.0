# Generated by Django 4.0.8 on 2022-11-17 18:49

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('agronomia', 'AGRONOMIA (COMUNA 15)'), ('almagro', 'ALMAGRO (COMUNA 5)'), ('balvanera', 'BALVANERA (COMUNA 3)'), ('barracas', 'BARRACAS (COMUNA 4)'), ('belgrano', 'BELGRANO (COMUNA 13)'), ('boca', 'BOCA (COMUNA 4)'), ('boedo', 'BOEDO (COMUNA 5)'), ('caballito', 'CABALLITO (COMUNA 6)'), ('chacarita', 'CHACARITA (COMUNA 15)'), ('coghlan', 'COGHLAN (COMUNA 12)'), ('colegiales', 'COLEGIALES (COMUNA 13)'), ('constitucion', 'CONSTITUCION (COMUNA 1)'), ('flores', 'FLORES (COMUNA 10)'), ('floresta', 'FLORESTA (COMUNA 10)'), ('liniers', 'LINIERS (COMUNA 9)'), ('mataderos', 'MATADEROS (COMUNA 9)'), ('monserrat', 'MONTSERRAT (COMUNA 1)'), ('monte-castro', 'MONTE CASTRO (COMUNA 10)'), ('nueva-pompeya', 'NUEVA POMPEYA (COMUNA 4)'), ('nunez', 'NUÑEZ (COMUNA 13)'), ('palermo', 'PALERMO (COMUNA 14)'), ('parque-avellaneda', 'PARQUE AVELLANEDA (COMUNA 9)'), ('parque-chacabuco', 'PARQUE CHACABUCO (COMUNA 7)'), ('parque-chas', 'PARQUE CHAS (COMUNA 15)'), ('parque-patricios', 'PARQUE PATRICIOS (COMUNA 4)'), ('paternal', 'PATERNAL (COMUNA 15)'), ('puerto-madero', 'PUERTO MADERO (COMUNA 1)'), ('recoleta', 'RECOLETA (COMUNA 2)'), ('retiro', 'RETIRO(COMUNA 1)'), ('saavedra', 'SAAVEDRA (COMUNA 12)'), ('san-cristobal', 'SAN CRISTOBAL (COMUNA 3)'), ('san-nicolas', 'SAN NICOLAS (COMUNA 1)'), ('san-telmo', 'SAN TELMO (COMUNA 1)'), ('velez-sarfield', 'VELEZ SARFIELD (COMUNA 10)'), ('versalles', 'VERSALLES (COMUNA 10)'), ('villa-crespo', 'VILLA CRESPO (COMUNA 15 )'), ('villa-del-parque', 'VILLA DEL PARQUE (COMUNA 11 )'), ('villa-devoto', 'VILLA DEVOTO (COMUNA 11 )'), ('villa-gral-mitre', 'VILLA GRAL. MITRE (COMUNA 11 )'), ('villa-lugano', 'VILLA LUGANO (COMUNA 8 )'), ('villa-luro', 'VILLA LURO (COMUNA 10 )'), ('villa-ortuzar', 'VILLA ORTUZAR (COMUNA 15 )'), ('villa-pueyrredon', 'VILLA PUEYRREDON (COMUNA 12 )'), ('villa-real', 'VILLA REAL (COMUNA 10 )'), ('villa-riachuelo', 'VILLA RIACHUELO (COMUNA 8 )'), ('villa-santa-rita', 'VILLA SANTA RITA (COMUNA 11 )'), ('villa-soldati', 'VILLA SOLDATI (COMUNA 8)'), ('villa-urquiza', 'VILLA URQUIZA(COMUNA 12 )')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.IntegerField(choices=[(1, 'Milagros'), (2, 'Carolina'), (3, 'Monica')], null=True)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('MUJER', 'Mujer'), ('HOMBRE', 'Hombre'), ('NO RESPONDE', 'No responde')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('gel_nail', 'Gel nail'), ('kapping_nail', 'Kapping nail'), ('acrylic_nail', 'Acrylic nail'), ('lifting', 'Lifting lashes'), ('extension', 'Extension lashes'), ('perfilado_cejas', 'Perfilado de cejas'), ('threading_cejas', 'Threading de cejas'), ('facial', 'Tratamiento facial'), ('acido_hialuronico', 'Acido hialuronico')], max_length=50)),
                ('duration', models.PositiveBigIntegerField(verbose_name='duracion')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Nombre de usuario')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='E-mail')),
                ('password', models.CharField(max_length=256, verbose_name='Contraseña')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Fecha inicio')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Ultimo inicio sesion')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Es admin')),
                ('is_active', models.BooleanField(default=True, verbose_name='Esta activo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Es staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Es superusuario')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='Nombre')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Apellido')),
                ('cellphone_number', models.CharField(blank=True, max_length=20, verbose_name='Número de teléfono')),
                ('address', models.CharField(blank=True, max_length=50, verbose_name='Dirección')),
                ('birth', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('profile_image', models.ImageField(blank=True, default=app.models.get_default_profile_image, max_length=255, null=True, upload_to=app.models.get_profile_image_filepath, verbose_name='Foto de perfil')),
                ('barrio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.barrio', verbose_name='Barrio')),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.genre', verbose_name='Género')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, help_text='DD-MM-AAAA')),
                ('timeslot', models.IntegerField(choices=[(1, '10:00 - 11:00'), (2, '11:00 - 12:00'), (3, '12:00 - 13:00'), (4, '13:00 - 14:00'), (5, '14:00 - 15:00'), (6, '15:00 - 16:00'), (7, '16:00 - 17:00'), (8, '17:00 - 18:00'), (9, '18:00 - 19:00')], default='Elija el horario', null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'date', 'timeslot')},
            },
        ),
    ]
