from django.shortcuts import render


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


# Datos de ejemplo hasta tener el modelo de servicios (Sprint 2).
SERVICIOS = [
    {
        'slug': 'construccion-desde-cero',
        'nombre': 'Construcción desde cero',
        'descripcion_corta': 'Obra nueva, desde los cimientos hasta los acabados.',
        'foto': 'img/servicios/construccion-desde-cero.svg',
    },
    {
        'slug': 'remodelacion',
        'nombre': 'Remodelación',
        'descripcion_corta': (
            'Renovamos espacios de tu casa o local para darles un nuevo uso '
            'o una nueva cara.'
        ),
        'foto': 'img/servicios/remodelacion.svg',
    },
    {
        'slug': 'estuco',
        'nombre': 'Estuco',
        'descripcion_corta': (
            'Preparamos y alisamos muros y techos para dejarlos listos para pintar.'
        ),
        'foto': 'img/servicios/estuco.svg',
    },
    {
        'slug': 'pintura',
        'nombre': 'Pintura',
        'descripcion_corta': (
            'Pintura de interiores y exteriores con un acabado parejo y limpio.'
        ),
        'foto': 'img/servicios/pintura.svg',
    },
    {
        'slug': 'pisos',
        'nombre': 'Pisos',
        'descripcion_corta': 'Instalación de pisos para interiores y exteriores.',
        'foto': 'img/servicios/pisos.svg',
    },
    {
        'slug': 'carpinteria',
        'nombre': 'Carpintería',
        'descripcion_corta': 'Trabajos en madera hechos a la medida de tu espacio.',
        'foto': 'img/servicios/carpinteria.svg',
    },
    {
        'slug': 'cerrajeria-en-aluminio',
        'nombre': 'Cerrajería en aluminio',
        'descripcion_corta': 'Ventanas, puertas y estructuras en aluminio.',
        'foto': 'img/servicios/cerrajeria-en-aluminio.svg',
    },
    {
        'slug': 'divisiones-de-bano',
        'nombre': 'Divisiones de baño',
        'descripcion_corta': (
            'Divisiones para duchas y baños, a la medida del espacio.'
        ),
        'foto': 'img/servicios/divisiones-de-bano.svg',
    },
    {
        'slug': 'asesoria-en-acabados',
        'nombre': 'Asesoría en acabados',
        'descripcion_corta': 'Te orientamos para elegir los acabados de tu obra.',
        'foto': 'img/servicios/asesoria-en-acabados.svg',
    },
]


def servicios(request):
    contexto = {'servicios': SERVICIOS}
    return render(request, 'sitio/servicios.html', contexto)


def galeria(request):
    return render(request, 'sitio/galeria.html')


def quienes_somos(request):
    return render(request, 'sitio/quienes_somos.html')


def contacto(request):
    return render(request, 'sitio/contacto.html')
