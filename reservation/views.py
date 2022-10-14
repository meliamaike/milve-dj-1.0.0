from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Employee, Booking, Service
from .forms import AvailabilityForm
from reservation.booking_functions.availability import check_availability 
# Create your views here.

def ServiceListView(request):
    service = Service.objects.all()[0]
    service_categories=dict(service.SERVICE_CATEGORIES)
    service_values = service_categories.values()
    service_list=[]
    for service_category in service_categories:
        service = service_categories.get(service_category)
        service_url= reverse('reservation:ServiceDetailView', 
                              kwargs={'category':service_category})
        service_list.append((service,service_url))
                
    context={
        "service_list" : service_list,
    }
    return render(request, 'service_list_view.html', context)

class EmployeeList(ListView):
    model=Employee

class BookingListView(ListView):
    model=Booking
    template_name = "booking_list_view.html"
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list=Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list
            
class ServiceDetailView(View):
   
    def get(self,request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form=AvailabilityForm()
        service_list = Service.objects.filter(category=category)
        
        if len(service_list)>0:
            service = service_list[0]
            service_category=dict(service.SERVICE_CATEGORIES).get(service.category, None)
            context ={
                'service_category': service_category,
                'form' : form
            }
            return render(request, 'service_detail_view.html', context)
        else:
            return HttpResponse('No existe la categoria')
    
    
    
    def post(self,request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        service_list = Service.objects.filter(category=category)
        form =AvailabilityForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
        
        available_services=[]
        for s in service_list:
            if check_availability(s, data['check_in'], data['check_out']):
                available_services.append(s)
        
        if len(available_services)>0:
            service= available_services[0]
            booking = Booking.objects.create(
                user= self.request.user,
                service=service,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('Este servicio se encuentra lleno.')

class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('reservation:BookingListView')
