from django.urls import path 
from .views import EmployeeList, BookingListView, ServiceListView, ServiceDetailView, CancelBookingView
app_name = 'reservation'

urlpatterns=[
    path('employee_list/', EmployeeList.as_view(), name = 'EmployeeList'),
    path('service_list/', ServiceListView, name = 'ServiceListView'),
    path('booking_list/', BookingListView.as_view(), name = 'BookingListView'),
    path('service/<category>', ServiceDetailView.as_view(), name = 'ServiceDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name = 'CancelBookingView')

]