from django.urls import path
from .views import (
    Index,
    register_request,
    login_request,
    logout_request,
    EmployeeList,
    BookingListView,
    ServiceListView,
    ServiceDetailView,
    CancelBookingView,
    password_reset_request,
    contact,
    new_appointment
)

app_name = "app"

urlpatterns = [
    path("", Index, name="index"),
    path("logout/", logout_request, name="LogoutView"),
    path("register/", register_request, name="RegisterView"),
    path("login/", login_request, name="LoginView"),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('newapo/', new_appointment),
    path("employee_list/", EmployeeList.as_view(), name="EmployeeList"),
    path("service_list/", ServiceListView, name="ServiceListView"),
    path("booking_list/", BookingListView.as_view(), name="BookingListView"),
    path("service/<category>", ServiceDetailView.as_view(), name="ServiceDetailView"),
    path("booking/cancel/<pk>", CancelBookingView.as_view(), name="CancelBookingView"),
]
