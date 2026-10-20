from django.test import TestCase
from django.urls import reverse


class PageTests(TestCase):
    def assert_page_renders(self, url_name):
        response = self.client.get(reverse(f'sitio:{url_name}'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_inicio(self):
        self.assert_page_renders('inicio')

    def test_servicios(self):
        self.assert_page_renders('servicios')

    def test_galeria(self):
        self.assert_page_renders('galeria')

    def test_quienes_somos(self):
        self.assert_page_renders('quienes_somos')

    def test_contacto(self):
        self.assert_page_renders('contacto')
