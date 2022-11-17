from django.urls import path, register_converter
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
    new_appointment,
    profile,
    ChangePasswordView,
    details_appointment,
    cancel_appointment,
    statistics,
    all_appointment,
)

app_name = "app"

urlpatterns = [
    path("", Index, name="index"),
    path("logout/", logout_request, name="LogoutView"),
    path("register/", register_request, name="RegisterView"),
    path("login/", login_request, name="LoginView"),
    path("password_reset/", password_reset_request, name="password_reset"),
    path("booking/new/", new_appointment),
    path("booking/all/", all_appointment),
    path("booking/details/", BookingListView.as_view(), name="BookingListView"),
    path("booking/cancel/<pk>", CancelBookingView.as_view(), name="CancelBookingView"),
    path("statistic/", statistics),
    path("profile/", profile, name="users-profile"),
    path("password-change/", ChangePasswordView.as_view(), name="password_change"),
    path("employee_list/", EmployeeList.as_view(), name="EmployeeList"),
    path("service_list/", ServiceListView, name="ServiceListView"),
    path("service/<category>", ServiceDetailView.as_view(), name="ServiceDetailView"),
   
]
