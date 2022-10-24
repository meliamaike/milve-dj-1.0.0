from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, FormView, View, DeleteView

from django.urls import reverse, reverse_lazy
from .models import Employee, Booking, Service, User
from .forms import AvailabilityForm, RegistrationForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib import messages
from app.booking_functions.availability import check_availability
from app.booking_functions.get_service_cat_url_list import (
    get_service_cat_url_list,
)
from app.booking_functions.get_service_category_human_format import (
    get_service_category_human_format,
)
from app.booking_functions.get_available_services import get_available_service

# Olvido de contrasena
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Vistas


def Index(request):
    return render(request, "home.html")


def register_request(request):
    user = request.user
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "Se ha registrado exitosamente.")
            return redirect("/")
        messages.error(request, "Error.")
    form = RegistrationForm()
    return render(
        request=request, template_name="register.html", context={"register_form": form}
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(
                    request,
                    user,
                    backend="allauth.account.auth_backends.AuthenticationBackend",
                )
                messages.info(request, f"Hola {username}.")
                return redirect("/")
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "Ha cerrado sesion correctamente.")
    return redirect("/")


# Olvido de contraseña


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Cambio de contraseña"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Estetica Milagros Veliz",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "hola@milve.com",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )


def RegisterView(request):
    return render(request, "register.html")


def ServiceListView(request):

    service_category_url_list = get_service_cat_url_list()

    context = {"service_list": service_category_url_list}
    return render(request, "service_list_view.html", context)


class EmployeeList(ListView):
    model = Employee


class BookingListView(ListView):
    model = Booking
    template_name = "booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class ServiceDetailView(View):
    def get(self, request, *args, **kwargs):

        # Traigo las categorias de los servicios a traves de los kwargs
        category = self.kwargs.get("category", None)
        # Traigo formato amigable con el ser humano
        human_format_service_category = get_service_category_human_format(category)
        # Inicializo un formulario vacio
        form = AvailabilityForm()
        # Me fijo si se ingresan categorias inavalidas
        if human_format_service_category is not None:
            context = {"service_category": human_format_service_category, "form": form}
            return render(request, "service_detail_view.html", context)
        else:
            return HttpResponse("No existe la categoria.")

    def post(self, request, *args, **kwargs):
        # Traigo las categorias de los servicios a traves de los kwargs
        category = self.kwargs.get("category", None)
        form = AvailabilityForm(request.POST)

        # Chequea si es valido o no
        if form.is_valid():
            data = form.cleaned_data

        # Trae los servicios disponibles
        available_services = get_available_service(
            category, data["check_in"], data["check_out"]
        )

        # Chequea si los servicios estan disponibles
        if available_services is not None:

            # Reserva un servicio
            booking = book_service(
                request, available_services[0], data["check_in"], data["check_out"]
            )
            return HttpResponse(booking)
        else:
            return HttpResponse("Este servicio se encuentra lleno.")


class CancelBookingView(DeleteView):
    model = Booking
    template_name = "booking_cancel_view.html"
    success_url = reverse_lazy("app:BookingListView")
