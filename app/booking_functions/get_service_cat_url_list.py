from app.models import Service
from django.urls import reverse


def get_service_cat_url_list():

    """
    La funcion devuelve la Lista de las categorias de los distintos servicios y sus correspondientes URLs
    """
    service = Service.objects.all()[0]  # Obtengo objectos de tipo Servicio
    service_categories = dict(
        service.SERVICE_CATEGORIES
    )  # Hago un diccionario a partir de la tupla "SERVICE CATEGORIES" en la clase "Servicio"
    service_cat_url_list = (
        []
    )  # Lista para guardar Servicios en el formato (categoria,URL)

    for category in service_categories:
        service_category = service_categories.get(category)
        service_url = reverse("app:ServiceDetailView", kwargs={"category": category})
        service_cat_url_list.append((service_category, service_url))
    return service_cat_url_list
