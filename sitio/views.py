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


def servicios(request):
    return render(request, 'sitio/servicios.html')


def galeria(request):
    return render(request, 'sitio/galeria.html')


def quienes_somos(request):
    return render(request, 'sitio/quienes_somos.html')


def contacto(request):
    return render(request, 'sitio/contacto.html')
