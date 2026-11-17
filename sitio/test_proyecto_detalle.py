import re
import shutil
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import FotoProyecto
from .test_galeria import crear_foto, crear_proyecto

# Carpeta temporal para las fotos que crean las pruebas; se borra al terminar.
MEDIA_TEMPORAL = tempfile.mkdtemp(prefix='adb-detalle-')


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class DetalleTestCase(TestCase):
    """Base de las pruebas de la página del proyecto."""

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def abrir(self, proyecto):
        response = self.client.get(proyecto.get_absolute_url())
        return response, response.content.decode()


class DetalleDelProyectoTests(DetalleTestCase):
    """HU-14 · Detalle de un proyecto."""

    def setUp(self):
        self.proyecto = crear_proyecto(
            'cocina-de-prueba',
            nombre='Cocina de prueba',
            servicio='remodelacion',
            descripcion='Primer párrafo de la obra.\n\nSegundo párrafo.',
        )
        self.antes = crear_foto(
            self.proyecto,
            FotoProyecto.Tipo.ANTES,
            orden=0,
            descripcion='Cocina antes de la obra',
        )
        self.despues = crear_foto(
            self.proyecto,
            FotoProyecto.Tipo.DESPUES,
            orden=1,
            descripcion='Cocina terminada',
        )
        self.response, self.html = self.abrir(self.proyecto)

    def test_responde_200_y_usa_la_plantilla_del_detalle(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'sitio/proyecto_detalle.html')

    def test_tiene_un_solo_h1_con_el_nombre_del_proyecto(self):
        self.assertEqual(self.html.count('<h1'), 1)
        self.assertIn(
            '<h1 id="proyecto-titulo">Cocina de prueba</h1>',
            self.html,
        )

    def test_el_titulo_de_la_pagina_lleva_el_nombre(self):
        self.assertIn(
            '<title>Cocina de prueba | Alexander Drada</title>',
            self.html,
        )

    def test_muestra_la_descripcion_con_sus_parrafos(self):
        self.assertContains(self.response, '<p>Primer párrafo de la obra.</p>')
        self.assertContains(self.response, '<p>Segundo párrafo.</p>')

    def test_muestra_el_servicio_con_enlace_al_filtro_de_la_galeria(self):
        self.assertIn(
            '<a class="proyecto-detalle__servicio" '
            'href="/galeria/?servicio=remodelacion">Remodelación</a>',
            self.html,
        )

    def test_la_foto_principal_es_la_portada_del_proyecto(self):
        principal = re.search(
            r'<a class="proyecto__ampliar proyecto__ampliar--principal"'
            r'[^>]*>',
            self.html,
        )

        self.assertIsNotNone(principal)
        self.assertIn(self.proyecto.foto_portada.imagen.url, principal.group(0))

    def test_cada_foto_es_un_enlace_ampliable_con_su_alt(self):
        for foto in (self.antes, self.despues):
            with self.subTest(foto=foto.descripcion):
                enlace = re.search(
                    r'<a class="proyecto__ampliar" '
                    rf'href="{re.escape(foto.imagen.url)}" data-ampliar '
                    rf'data-alt="{re.escape(foto.descripcion)}">',
                    self.html,
                )
                self.assertIsNotNone(enlace)
                self.assertIn(
                    f'<img src="{foto.imagen.url}" '
                    f'alt="{foto.descripcion}"',
                    self.html,
                )

    def test_existe_el_visor_y_se_carga_el_javascript(self):
        self.assertEqual(self.html.count('<dialog'), 1)
        self.assertIn('<dialog class="visor"', self.html)
        self.assertIn('class="visor__imagen"', self.html)
        self.assertIn('class="visor__cerrar"', self.html)
        self.assertIn('js/proyecto_detalle.js', self.html)
        self.assertIn('css/proyecto_detalle.css', self.html)

    def test_hay_enlace_para_volver_a_la_galeria(self):
        self.assertIn(
            '<a class="proyecto-detalle__volver" href="/galeria/">'
            'Volver a la galería</a>',
            self.html,
        )
        self.assertEqual(self.response.context['url_volver'], '/galeria/')

    def test_las_migas_enlazan_a_la_galeria(self):
        self.assertIn('<a href="/galeria/">Galería</a>', self.html)

    def test_en_el_menu_galeria_queda_marcada_como_actual(self):
        enlace = re.search(
            r'<a class="nav__link" href="/galeria/"[^>]*>Galería</a>',
            self.html,
        )

        self.assertIsNotNone(enlace)
        self.assertIn('aria-current="page"', enlace.group(0))

    def test_en_el_menu_solo_galeria_queda_marcada(self):
        self.assertEqual(self.html.count('aria-current="page"'), 1)

    def test_un_proyecto_no_publicado_responde_404(self):
        oculto = crear_proyecto('oculto', publicado=False)

        response, _ = self.abrir(oculto)

        self.assertEqual(response.status_code, 404)

    def test_un_slug_inexistente_responde_404(self):
        response = self.client.get('/galeria/no-existe/')

        self.assertEqual(response.status_code, 404)

    def test_un_proyecto_sin_fotos_responde_200_con_la_imagen_de_reemplazo(self):
        vacio = crear_proyecto('sin-fotos', nombre='Sin fotos')

        response, html = self.abrir(vacio)

        self.assertEqual(response.status_code, 200)
        self.assertIn('img/galeria/sin-foto.svg', html)
        self.assertNotIn('data-ampliar', html)

    def test_una_descripcion_con_html_se_muestra_como_texto(self):
        peligroso = crear_proyecto(
            'con-html',
            descripcion='<script>alert(1)</script>',
        )

        _, html = self.abrir(peligroso)

        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', html)


class DetalleSinPreciosTests(DetalleTestCase):
    def test_la_pagina_del_proyecto_no_muestra_montos(self):
        proyecto = crear_proyecto('con-fotos', nombre='Con fotos')
        crear_foto(proyecto, FotoProyecto.Tipo.ANTES)
        crear_foto(proyecto, FotoProyecto.Tipo.DESPUES, orden=1)

        _, html = self.abrir(proyecto)

        self.assertIsNone(re.search(r'\$\s?\d', html))
        self.assertIsNone(re.search(r'\d\s?(COP|pesos)', html, re.IGNORECASE))
