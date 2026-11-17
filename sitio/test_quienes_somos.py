import re

from django.test import TestCase
from django.urls import reverse


class QuienesSomosTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('sitio:quienes_somos'))
        self.html = self.response.content.decode()

    def test_responde_y_usa_la_plantilla(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'sitio/quienes_somos.html')

    def test_un_solo_h1(self):
        self.assertEqual(self.html.count('<h1'), 1)

    def test_contenido_principal(self):
        for texto in (
            'Alexander Drada',
            'Nuestra forma de trabajar',
            'Calidad',
            'Cumplimiento',
            'Experiencia',
        ):
            self.assertContains(self.response, texto)

    def test_enlaces_a_galeria_y_contacto(self):
        for nombre in ('galeria', 'contacto'):
            self.assertContains(
                self.response, f'href="{reverse(f"sitio:{nombre}")}"'
            )

    def test_sin_precios(self):
        self.assertNotIn('$', self.html)

    def test_experiencia_sin_cifras(self):
        seccion = self.html.split('id="experiencia-titulo"')[1]
        seccion = seccion.split('</section>')[0]
        texto = re.sub(r'<[^>]+>', '', seccion)
        self.assertIsNone(re.search(r'\d', texto))
