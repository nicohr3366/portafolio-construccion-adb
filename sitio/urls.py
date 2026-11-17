from django.urls import path

from . import views

app_name = 'sitio'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path(
        'servicios/<slug:slug>/',
        views.servicio_detalle,
        name='servicio_detalle',
    ),
    path('galeria/', views.galeria, name='galeria'),
    path(
        'galeria/<slug:slug>/',
        views.proyecto_detalle,
        name='proyecto_detalle',
    ),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('contacto/', views.contacto, name='contacto'),
]
