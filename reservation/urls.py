from django.urls import path
from .views import (
    HomeView,
    LogoutView,
    register_request,
    login_request,
    logout_request,
    EmployeeList,
    BookingListView,
    ServiceListView,
    ServiceDetailView,
    CancelBookingView,
)

app_name = "reservation"

urlpatterns = [
    path("", HomeView, name="HomeView"),
    path("logout/", LogoutView, name="LogoutView"),
    path("register/", register_request, name="RegisterView"),
    path("login/", login_request, name="LoginView"),
    path("logout", logout_request, name= "LogoutView"),
    path("employee_list/", EmployeeList.as_view(), name="EmployeeList"),
    path("service_list/", ServiceListView, name="ServiceListView"),
    path("booking_list/", BookingListView.as_view(), name="BookingListView"),
    path("service/<category>", ServiceDetailView.as_view(), name="ServiceDetailView"),
    path("booking/cancel/<pk>", CancelBookingView.as_view(), name="CancelBookingView"),
]
