from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from requests import request
from .models import Booking, Service, User, Employee
from .forms import (
    AvailabilityForm,
    RegistrationForm,
    ContactForm,
    BookingForm,
    UpdateUserForm,
)
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
from app.booking_functions.book_service import book_service

# Olvido de contrasena
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from datetime import date

# Vistas


def Index(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, "admin@example.com", ["admin@example.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("main:homepage")

    form = ContactForm()
    return render(request, "home.html", {"form": form})


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
                messages.error(request, "E-mail o contraseña incorrectos.")
        else:
            messages.error(request, "E-mail o contraseña incorrectos.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )


# Cerrar sesion
def logout_request(request):
    logout(request)
    messages.info(request, "Ha cerrado sesion correctamente.")
    return redirect("/")


def homepage(request):
    return render(request=request, template_name="home.html")


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
                        return HttpResponse("Se encontro una cabecera invalida..")
                    # return redirect("/password_reset/done/")
                    messages.success(
                        request,
                        "Se te ha enviado un e-mail con las instrucciones para poder resetear la contraseña.",
                    )
                    return redirect("app:index")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )


def RegisterView(request):
    return render(request, "register.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                "Nombre": form.cleaned_data["first_name"],
                "Apellido": form.cleaned_data["last_name"],
                "E-mail": form.cleaned_data["email"],
                "Mensaje": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, "hola@milve.com", ["admin@example.com"])
            except BadHeaderError:
                return HttpResponse("Se encontro una cabecera invalida.")
            return redirect("index")

    form = ContactForm()
    return render(request, "home.html", {"form": form})


def ServiceListView(request):

    service_category_url_list = get_service_cat_url_list()
    context = {"service_list": service_category_url_list}
    return render(request, "service_list_view.html", context)


class EmployeeList(ListView):
    model = Employee


class BookingListView(ListView):
    model = Booking
    template_name = "appointment_details.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.filter(date__gte=date.today()).order_by(
                "date", "timeslot"
            )
            return booking_list
        else:
            booking_list = Booking.objects.filter(
                user=self.request.user, date__gte=date.today()
            ).order_by("date", "timeslot")
            return booking_list


class AllBookingListView(ListView):
    model = Booking
    template_name = "appointment_all.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.filter(date__gte=date.today()).order_by(
                "date", "timeslot"
            )
            return booking_list


def details_appointment(request):
    return render(request=request, template_name="appointment_details.html")


def cancel_appointment(request):
    return render(request=request, template_name="appointment_cancel.html")


def statistics(request):
    return render(request=request, template_name="statistics.html")


def all_appointment(request):
    return render(request=request, template_name="appointment_all.html")


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
            booking = book_service(request, available_services[0], data["check_in"])
            return HttpResponse(booking)
        else:
            messages.info(request, "Este servicio se encuentra lleno.")
            return render("/booking/new")


class CancelBookingView(DeleteView):
    model = Booking
    template_name = "appointment_cancel.html"
    success_url = reverse_lazy("app:BookingListView")
    success_message = "Se ha cancelado el turno."


def new_appointment(request):
    turn_form = BookingForm
    form = turn_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            available_day_turn = check_day_availability(
                data["date"],
            )
            if available_day_turn is True:
                available_turn = check_availability(
                    data["date"],
                    data["timeslot"],
                )

                if available_turn is True:

                    print(data["service"].id)

                    book_service(
                        request,
                        data["date"],
                        data["timeslot"],
                        data["service"].id,
                        request.user.id,
                    )
                    # form.save()
                    return redirect("/")
                else:
                    messages.error(request, "Este horario esta ocupado.")
                    return redirect("/booking/new/")
            else:
                messages.success(request, "No existen turnos disponibles este dia")
                return redirect("/booking/new/")
    return render(
        request=request,
        template_name="appointment_form.html",
        context={"form": form},
    )


def check_day_availability(date):

    turn_list = Booking.objects.all()
    cont = 0

    for t in turn_list:
        if t.date == date:
            cont = cont + 1

    if cont == 7:
        return False
    else:
        return True


def check_availability(date, timeslot):

    turn = Booking.objects.all()
    new_turn = None

    for t in turn:
        if t.date == date and t.timeslot == timeslot:
            new_turn = t

    if new_turn != None:
        return False
    else:
        return True


def book_service(request, date, timeslot, service_id, user_id):
    # Crea un objeto de tipo Booking y lo guarda

    print(request.user.id)
    turn = Booking.objects.create(
        date=date, timeslot=timeslot, service_id=service_id, user_id=user_id
    )
    turn.save()
    messages.success(request, "Se ha realizado la reserva correctamente.")
    return turn


# Mi perfil
@login_required
def profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Se ha actualizado tu perfil exitosamente.")
            return redirect("/profile")
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(
        request, template_name="profile.html", context={"user_form": user_form}
    )


# Cambiar la password desde "Mi Perfil"
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "change_password.html"
    success_message = "Se ha actualizado exitosamente la contraseña."
    success_url = reverse_lazy("index")
