from django.test import TestCase
from django.urls import reverse

from .views import SERVICIOS


class CatalogoServiciosTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('sitio:servicios'))
        self.html = self.response.content.decode()

    def test_responde_y_usa_la_plantilla(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'sitio/servicios.html')

    def test_titulo_de_la_seccion(self):
        self.assertContains(self.response, 'Nuestros servicios')
        self.assertEqual(self.html.count('<h1'), 1)

    def test_estan_los_nueve_servicios(self):
        self.assertEqual(len(SERVICIOS), 9)
        for servicio in SERVICIOS:
            self.assertContains(self.response, servicio['nombre'])

    def test_servicios_en_el_orden_definido(self):
        posiciones = [self.html.index(servicio['nombre']) for servicio in SERVICIOS]
        self.assertEqual(posiciones, sorted(posiciones))

    def test_servicios_sin_duplicados(self):
        slugs = [servicio['slug'] for servicio in SERVICIOS]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_nueve_tarjetas_con_nombre_y_descripcion(self):
        self.assertEqual(self.html.count('class="servicio-card"'), 9)
        for servicio in SERVICIOS:
            self.assertContains(self.response, servicio['descripcion_corta'])

    def test_imagenes_apuntan_a_los_svg_de_cada_servicio(self):
        for servicio in SERVICIOS:
            self.assertIn(
                f'src="/static/{servicio["foto"]}"',
                self.html,
            )
            self.assertTrue(servicio['foto'].endswith('.svg'))
