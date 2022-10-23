from app.models import Service


def get_service_category_human_format(category):

    """
    Toma el formato abreviado de las categorias de los servicios y lo lleva a un formato amigable con el ser humano
    """
    service = Service.objects.all()[0]
    service_category = dict(service.SERVICE_CATEGORIES).get(category, None)
    return service_category
