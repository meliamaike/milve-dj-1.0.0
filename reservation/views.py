from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Employee, Booking, Service
from .forms import AvailabilityForm, NewUserForm
from django.contrib.auth import login, authenticate,logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from reservation.booking_functions.availability import check_availability
from reservation.booking_functions.get_service_cat_url_list import (
    get_service_cat_url_list,
)
from reservation.booking_functions.get_service_category_human_format import (
    get_service_category_human_format,
)
from reservation.booking_functions.get_available_services import get_available_service


# Vistas


def HomeView(request):
    return render(request, "home.html")


def LogoutView(request):
    return render(request, "home.html")


def LoginView(request):
    return render(request, "login.html")

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Se ha registrado exitosamente.")
            return redirect("/")
        messages.error(request, "Error.")
    form = NewUserForm()
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
                login(request, user)
                messages.info(request, f"Hola {username}.")
                return redirect("/")
            else:
                messages.error(request, "Usuario o password incorrectos.")
        else:
            messages.error(request, "Usuario o password incorrectos.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )

def logout_request(request):
	logout(request)
	messages.info(request, "Ha cerrado sesion correctamente.") 
	return redirect("/")

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
    success_url = reverse_lazy("reservation:BookingListView")
