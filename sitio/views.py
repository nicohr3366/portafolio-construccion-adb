from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .catalogo import SERVICIOS
from .models import Proyecto


# Datos de ejemplo hasta tener el modelo de proyectos (HU-25, HU-29).
PROYECTOS_DESTACADOS_EJEMPLO = [
    {
        'nombre': 'Remodelación de cocina',
        'tipo': 'Remodelación',
        'imagen': 'img/destacados/ejemplo-1.svg',
    },
    {
        'nombre': 'Casa de dos pisos',
        'tipo': 'Construcción',
        'imagen': 'img/destacados/ejemplo-2.svg',
    },
    {
        'nombre': 'Piso en porcelanato',
        'tipo': 'Acabados',
        'imagen': 'img/destacados/ejemplo-3.svg',
    },
]


def inicio(request):
    contexto = {'proyectos_destacados': PROYECTOS_DESTACADOS_EJEMPLO}
    return render(request, 'sitio/inicio.html', contexto)


def servicios(request):
    contexto = {'servicios': SERVICIOS}
    return render(request, 'sitio/servicios.html', contexto)


def servicio_detalle(request, slug):
    servicio = next(
        (item for item in SERVICIOS if item['slug'] == slug),
        None,
    )
    if servicio is None:
        raise Http404('El servicio no existe.')
    contexto = {'servicio': servicio}
    return render(request, 'sitio/servicio_detalle.html', contexto)


def galeria(request):
    return render(request, 'sitio/galeria.html')


def proyecto_detalle(request, slug):
    proyecto = get_object_or_404(
        Proyecto.objects.prefetch_related('fotos'),
        slug=slug,
        publicado=True,
    )

    return render(
        request,
        'sitio/proyecto_detalle.html',
        {'proyecto': proyecto}
    )


def quienes_somos(request):
    return render(request, 'sitio/quienes_somos.html')


def contacto(request):
    return render(request, 'sitio/contacto.html')
