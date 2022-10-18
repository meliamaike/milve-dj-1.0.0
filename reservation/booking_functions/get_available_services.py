from reservation.models import Service
from .availability import check_availability

def get_available_service(category, check_in, check_out):
    #Toma la categoria de servicios y devuelve una lista con estos
    service_list = Service.objects.filter(category = category)
        
    # Creo una lista vacia
    available_services=[]

    #Lleno la lista
    for s in service_list:
        if check_availability(s, check_in, check_out):
            available_services.append(s)
    
    #Chequeo el largo de la lista
    if len(available_services) > 0 :
        return available_services
    else:
        return None
