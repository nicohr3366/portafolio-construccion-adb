from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .catalogo import SERVICIOS, nombre_servicio, opciones_servicio
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
    publicados = Proyecto.objects.filter(publicado=True)
    proyectos = publicados.prefetch_related('fotos')

    servicios_con_proyectos = set(
        publicados.values_list('servicio', flat=True)
    )

    filtros = [
        {'slug': slug, 'nombre': nombre}
        for slug, nombre in opciones_servicio()
        if slug in servicios_con_proyectos
    ]

    servicio_activo = request.GET.get('servicio', '')

    if servicio_activo not in servicios_con_proyectos:
        servicio_activo = ''

    if servicio_activo:
        proyectos = proyectos.filter(servicio=servicio_activo)

    proyectos = list(proyectos)

    contexto = {
        'proyectos': proyectos,
        'filtros': filtros,
        'servicio_activo': servicio_activo,
        'nombre_servicio_activo': nombre_servicio(servicio_activo),
        'antes_y_despues': [
            p for p in proyectos if p.tiene_antes_y_despues
        ],
    }

    return render(
        request,
        'sitio/galeria.html',
        contexto
    )


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
