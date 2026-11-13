from django.conf import settings
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


class ObraCompletaTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('sitio:servicios'))

    def test_bloque_dentro_de_servicios(self):
        self.assertContains(self.response, 'Obra completa hasta entrega de llaves')
        self.assertContains(
            self.response,
            'Un solo equipo para todo el proyecto, desde cero hasta la entrega de llaves.',
        )

    def test_seccion_con_titulo_asociado(self):
        self.assertContains(
            self.response,
            'class="obra-completa" aria-labelledby="obra-completa-titulo"',
        )


class FichaServicioTests(TestCase):
    def setUp(self):
        self.servicio = SERVICIOS[4]
        self.url = reverse('sitio:servicio_detalle', args=[self.servicio['slug']])
        self.response = self.client.get(self.url)
        self.html = self.response.content.decode()

    def test_responde_y_usa_la_plantilla(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'sitio/servicio_detalle.html')

    def test_miga_de_pan_servicios_y_nombre(self):
        self.assertIn('aria-label="Ruta de navegación"', self.html)
        self.assertIn(f'href="{reverse("sitio:servicios")}"', self.html)
        self.assertIn('<h1 id="servicio-titulo">', self.html)

    def test_ficha_con_foto_nombre_y_descripcion(self):
        self.assertIn(f'src="/static/{self.servicio["foto"]}"', self.html)
        self.assertEqual(self.html.count('<h1'), 1)
        self.assertContains(self.response, self.servicio['nombre'])
        self.assertContains(self.response, self.servicio['descripcion'])

    def test_enlace_volver_a_servicios(self):
        self.assertContains(self.response, 'Volver a Servicios')
        self.assertIn(f'href="{reverse("sitio:servicios")}"', self.html)

    def test_direccion_con_el_slug_del_servicio(self):
        self.assertEqual(self.url, f'/servicios/{self.servicio["slug"]}/')

    def test_servicio_inexistente_responde_404(self):
        response = self.client.get('/servicios/servicio-que-no-existe/')
        self.assertEqual(response.status_code, 404)


class FichasDeLosNueveServiciosTests(TestCase):
    def test_cada_servicio_tiene_descripcion_y_foto_marcador(self):
        for servicio in SERVICIOS:
            self.assertTrue(servicio['descripcion'].strip())
            self.assertTrue(servicio['foto'].startswith('img/servicios/'))
            self.assertTrue(servicio['foto'].endswith('.svg'))

    def test_cada_ficha_muestra_su_propia_informacion(self):
        for servicio in SERVICIOS:
            url = reverse('sitio:servicio_detalle', args=[servicio['slug']])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, f'<h1 id="servicio-titulo">{servicio["nombre"]}</h1>', html=False)
            self.assertContains(response, servicio['descripcion'])
            for otro in SERVICIOS:
                if otro['slug'] != servicio['slug']:
                    self.assertNotContains(response, otro['descripcion'])

    def test_catalogo_enlaza_cada_tarjeta_con_su_ficha(self):
        response = self.client.get(reverse('sitio:servicios'))
        html = response.content.decode()
        self.assertEqual(html.count('class="servicio-card__enlace"'), 9)
        for servicio in SERVICIOS:
            url = reverse('sitio:servicio_detalle', args=[servicio['slug']])
            self.assertIn(f'href="{url}"', html)

    def test_textos_provisionales_marcados_en_las_plantillas(self):
        plantillas = (
            'sitio/templates/sitio/servicios.html',
            'sitio/templates/sitio/servicio_detalle.html',
        )
        for ruta in plantillas:
            contenido = (settings.BASE_DIR / ruta).read_text(encoding='utf-8')
            self.assertIn('{# POR DEFINIR con Alexander #}', contenido)
