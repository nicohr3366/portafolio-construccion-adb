from django.shortcuts import render


def inicio(request):
    return render(request, 'sitio/inicio.html')


def servicios(request):
    return render(request, 'sitio/servicios.html')


def galeria(request):
    return render(request, 'sitio/galeria.html')


def quienes_somos(request):
    return render(request, 'sitio/quienes_somos.html')


def contacto(request):
    return render(request, 'sitio/contacto.html')
