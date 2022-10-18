from reservation.models import Booking, Service

def book_service(request, service, check_in, check_out):
    #Crea un objeto de tipo Booking y lo guarda
    booking = Booking.objects.create(
        user = request.user,
        service = service,
        check_in = check_in,
        check_out = check_out
    )
    booking.save()
    
    return booking