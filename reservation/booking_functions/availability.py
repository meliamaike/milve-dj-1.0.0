import datetime
from reservation.models import Employee, Booking, Service


def check_availability(service, check_in, check_out):
    avail_list = []
    booking_list = Booking.objects.filter(service=service)
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)
