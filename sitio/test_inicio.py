from django.test import TestCase
from django.urls import reverse

from .views import PROYECTOS_DESTACADOS_EJEMPLO


class InicioTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('sitio:inicio'))
        self.html = self.response.content.decode()

    def test_responde_y_usa_la_plantilla(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'sitio/inicio.html')

    def test_portada_con_nombre_frase_y_accesos(self):
        self.assertContains(self.response, 'Construcciones y Remodelaciones')
        self.assertContains(
            self.response,
            'Construimos y remodelamos con calidad y cumplimiento',
        )
        for nombre in ('servicios', 'galeria', 'contacto'):
            self.assertContains(
                self.response, f'href="{reverse(f"sitio:{nombre}")}"'
            )

    def test_un_solo_h1(self):
        self.assertEqual(self.html.count('<h1'), 1)

    def test_proyectos_destacados(self):
        proyectos = self.response.context['proyectos_destacados']
        self.assertGreaterEqual(len(proyectos), 3)
        for proyecto in proyectos:
            self.assertContains(self.response, proyecto['nombre'])
        self.assertEqual(proyectos, PROYECTOS_DESTACADOS_EJEMPLO)

    def test_imagenes_de_los_destacados(self):
        self.assertEqual(self.html.count('class="proyecto-card"'), 3)
        for proyecto in self.response.context['proyectos_destacados']:
            self.assertContains(self.response, proyecto['imagen'])

    def test_enlace_a_la_galeria_en_destacados(self):
        seccion = self.html.split('id="destacados-titulo"')[1]
        self.assertIn(f'href="{reverse("sitio:galeria")}"', seccion)
        self.assertIn('Ver galería completa', seccion)

    def test_sin_precios(self):
        self.assertNotIn('$', self.html)
        self.assertNotIn('precio', self.html.lower())
