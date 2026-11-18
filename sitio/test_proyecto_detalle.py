import html as html_utils
import re
import shutil
import tempfile
from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .catalogo import SERVICIOS
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


class ObraGrandeTests(DetalleTestCase):
    """HU-13 · Obras grandes con su proceso."""

    def setUp(self):
        self.obra = crear_proyecto(
            'obra-grande-de-prueba',
            nombre='Obra grande de prueba',
            servicio='construccion-desde-cero',
            es_obra_grande=True,
        )
        # Se crean desordenadas a propósito: la página debe respetar `orden`.
        crear_foto(self.obra, FotoProyecto.Tipo.DESPUES, orden=7,
                   descripcion='Final segunda')
        crear_foto(self.obra, FotoProyecto.Tipo.PROCESO, orden=3,
                   descripcion='Etapa tercera')
        crear_foto(self.obra, FotoProyecto.Tipo.ANTES, orden=0,
                   descripcion='Terreno antes')
        crear_foto(self.obra, FotoProyecto.Tipo.PROCESO, orden=1,
                   descripcion='Etapa primera')
        crear_foto(self.obra, FotoProyecto.Tipo.DESPUES, orden=5,
                   descripcion='Final primera')
        crear_foto(self.obra, FotoProyecto.Tipo.PROCESO, orden=2,
                   descripcion='Etapa segunda')
        self.response, self.html = self.abrir(self.obra)

    def test_las_secciones_salen_en_orden_antes_proceso_y_resultado(self):
        antes = self.html.index('<h2 id="titulo-antes">Antes</h2>')
        proceso = self.html.index('<h2 id="titulo-proceso">Proceso de obra</h2>')
        resultado = self.html.index('<h2 id="titulo-resultado">Resultado final</h2>')

        self.assertLess(antes, proceso)
        self.assertLess(proceso, resultado)

    def test_muestra_la_etiqueta_de_obra_de_gran_escala(self):
        self.assertIn(
            '<p class="proyecto__etiqueta">Obra de gran escala</p>',
            self.html,
        )

    def test_muestra_el_parrafo_provisional_de_la_obra(self):
        self.assertContains(
            self.response,
            'Así avanzó la obra, desde el proceso hasta el resultado final.',
        )

    def test_las_fotos_de_proceso_salen_como_etapas_respetando_el_orden(self):
        etapas = re.findall(
            r'<figure class="proyecto__etapa">.*?</figure>',
            self.html,
            re.DOTALL,
        )

        resumen = [
            (
                re.search(r'<img src="[^"]*" alt="([^"]*)"', etapa).group(1),
                re.search(r'<figcaption>([^<]*)</figcaption>', etapa).group(1),
            )
            for etapa in etapas
        ]
        self.assertEqual(resumen, [
            ('Etapa primera', 'Etapa 1'),
            ('Etapa segunda', 'Etapa 2'),
            ('Etapa tercera', 'Etapa 3'),
        ])

    def test_el_resultado_final_respeta_el_orden_de_las_fotos(self):
        inicio = self.html.index('id="titulo-resultado"')
        resultado = self.html[inicio:]

        self.assertLess(
            resultado.index('alt="Final primera"'),
            resultado.index('alt="Final segunda"'),
        )

    def test_con_antes_y_despues_aparece_el_bloque_comparativo(self):
        self.assertIn('<h2 id="titulo-comparacion">Antes y después</h2>', self.html)
        self.assertIn('class="antes-despues"', self.html)
        self.assertIn('<figcaption>Antes</figcaption>', self.html)
        self.assertIn('<figcaption>Después</figcaption>', self.html)
        self.assertLess(
            self.html.index('id="titulo-comparacion"'),
            self.html.index('id="titulo-antes"'),
        )
        self.assertIn('css/antes_despues.css', self.html)

    def test_un_proyecto_sin_fotos_de_proceso_no_muestra_esa_seccion(self):
        normal = crear_proyecto('sin-proceso', nombre='Sin proceso')
        crear_foto(normal, FotoProyecto.Tipo.ANTES)
        crear_foto(normal, FotoProyecto.Tipo.DESPUES, orden=1)

        _, html = self.abrir(normal)

        self.assertNotIn('Proceso de obra', html)
        self.assertNotIn('titulo-proceso', html)
        self.assertIn('Resultado final', html)

    def test_un_proyecto_normal_no_muestra_obra_de_gran_escala(self):
        normal = crear_proyecto('normal', nombre='Proyecto normal')
        crear_foto(normal, FotoProyecto.Tipo.DESPUES)

        _, html = self.abrir(normal)

        self.assertNotIn('Obra de gran escala', html)
        self.assertNotIn('Así avanzó la obra', html)

    def test_solo_aparecen_las_secciones_que_tienen_fotos(self):
        solo_despues = crear_proyecto('solo-despues', nombre='Solo después')
        crear_foto(solo_despues, FotoProyecto.Tipo.DESPUES)

        _, html = self.abrir(solo_despues)

        self.assertIn('titulo-resultado', html)
        self.assertNotIn('titulo-antes', html)
        self.assertNotIn('titulo-proceso', html)
        self.assertNotIn('titulo-comparacion', html)

    def test_un_proyecto_sin_antes_y_despues_no_muestra_el_comparativo(self):
        solo_antes = crear_proyecto('solo-antes', nombre='Solo antes')
        crear_foto(solo_antes, FotoProyecto.Tipo.ANTES)

        _, html = self.abrir(solo_antes)

        self.assertNotIn('Antes y después', html)
        self.assertIn('titulo-antes', html)

    def test_el_proyecto_de_ejemplo_muestra_toda_la_secuencia(self):
        call_command('cargar_proyectos_ejemplo', stdout=StringIO())
        response = self.client.get('/galeria/ejemplo-obra-grande/')
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Obra de gran escala', html)
        self.assertIn('<figcaption>Etapa 1</figcaption>', html)
        self.assertIn('<figcaption>Etapa 2</figcaption>', html)
        self.assertIn('<figcaption>Etapa 3</figcaption>', html)
        self.assertNotIn('Etapa 4', html)
        self.assertLess(html.index('titulo-antes'), html.index('titulo-proceso'))
        self.assertLess(html.index('titulo-proceso'), html.index('titulo-resultado'))

    def test_no_se_publican_nombres_reales_de_obras(self):
        call_command('cargar_proyectos_ejemplo', stdout=StringIO())
        html = self.client.get('/galeria/ejemplo-obra-grande/').content.decode()

        self.assertNotIn('Sagrada', html)
        self.assertNotIn('Colegio La', html)


class CotizacionDesdeProyectoTests(DetalleTestCase):
    """HU-16 · Pedir cotización desde un proyecto."""

    def setUp(self):
        self.proyecto = crear_proyecto(
            'cocina-de-prueba',
            nombre='Cocina de prueba',
            servicio='remodelacion',
        )
        crear_foto(self.proyecto, FotoProyecto.Tipo.DESPUES)
        self.url = (
            '/contacto/?servicio=remodelacion&proyecto=cocina-de-prueba'
            '#formulario-contacto'
        )
        self.response, self.html = self.abrir(self.proyecto)
        # En el HTML el & se escribe como &amp;.
        self.href = f'href="{html_utils.escape(self.url)}"'

    def test_la_vista_arma_la_direccion_de_cotizacion(self):
        self.assertEqual(self.response.context['url_cotizacion'], self.url)

    def test_el_boton_de_cotizacion_apunta_al_formulario_de_contacto(self):
        self.assertIn(
            f'<a class="boton-cotizacion proyecto__cotizar" {self.href}>'
            'Pedir cotización de un trabajo así</a>',
            self.html,
        )

    def test_el_boton_esta_cerca_del_titulo_antes_de_las_fotos(self):
        boton = self.html.index('Pedir cotización de un trabajo así')

        self.assertGreater(boton, self.html.index('<h1'))
        self.assertLess(boton, self.html.index('class="proyecto-detalle__foto"'))

    def test_aparece_el_bloque_como_se_cotiza_con_el_mismo_enlace(self):
        self.assertIn('<h2 id="cotizacion-titulo">¿Cómo se cotiza?</h2>', self.html)
        self.assertIn(
            f'<a class="boton-cotizacion" {self.href}>Pedir cotización</a>',
            self.html,
        )

    def test_los_dos_botones_llevan_a_la_misma_direccion(self):
        self.assertEqual(self.html.count(self.href), 2)

    def test_el_bloque_como_se_cotiza_va_al_final_de_la_pagina(self):
        self.assertGreater(
            self.html.index('id="cotizacion-titulo"'),
            self.html.index('Volver a la galería'),
        )

    def test_se_carga_el_estilo_de_cotizacion(self):
        self.assertIn('css/cotizacion.css', self.html)

    def test_el_enlace_lleva_el_servicio_de_cada_proyecto(self):
        for servicio in SERVICIOS:
            with self.subTest(servicio=servicio['slug']):
                proyecto = crear_proyecto(
                    f"obra-{servicio['slug']}",
                    servicio=servicio['slug'],
                )

                response, _ = self.abrir(proyecto)

                self.assertEqual(
                    response.context['url_cotizacion'],
                    f"/contacto/?servicio={servicio['slug']}"
                    f"&proyecto=obra-{servicio['slug']}#formulario-contacto",
                )

    def test_un_proyecto_sin_fotos_tambien_tiene_el_boton(self):
        vacio = crear_proyecto('sin-fotos', servicio='pintura')

        _, html = self.abrir(vacio)

        self.assertIn('Pedir cotización de un trabajo así', html)
        self.assertIn('¿Cómo se cotiza?', html)

    def test_el_recorrido_completo_llega_a_la_pagina_de_contacto(self):
        galeria = self.client.get(reverse('sitio:galeria'))
        self.assertContains(galeria, self.proyecto.get_absolute_url())

        detalle = self.client.get(self.proyecto.get_absolute_url())
        self.assertEqual(detalle.status_code, 200)

        # El navegador no envía la parte #formulario-contacto al servidor.
        contacto = self.client.get(self.url.split('#')[0])
        self.assertEqual(contacto.status_code, 200)
        self.assertTemplateUsed(contacto, 'sitio/contacto.html')

    def test_los_botones_no_muestran_precios(self):
        self.assertIsNone(re.search(r'\$\s?\d', self.html))
