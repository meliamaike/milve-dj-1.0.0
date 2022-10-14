from django.urls import path 
from .views import EmployeeList, BookingList, BookingView, ServiceListView, ServiceDetailView
app_name = 'reservation'

urlpatterns=[
    path('employee_list/', EmployeeList.as_view(), name = 'EmployeeList'),
    path('service_list/', ServiceListView, name = 'ServiceList'),
    path('booking_list/', BookingList.as_view(), name = 'BookingList'),
    path('book/', BookingView.as_view(), name = 'BookingView'),
    path('service/<category>', ServiceDetailView.as_view(), name = 'ServiceDetailView')

]