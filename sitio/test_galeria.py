import shutil
import tempfile
from io import BytesIO, StringIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .catalogo import SERVICIOS, opciones_servicio
from .models import FotoProyecto, Proyecto


def imagen_png():
    buffer = BytesIO()
    Image.new('RGB', (12, 8), (120, 120, 120)).save(buffer, format='PNG')
    return SimpleUploadedFile(
        'foto.png',
        buffer.getvalue(),
        content_type='image/png',
    )


class MediaTemporalMixin:
    @classmethod
    def setUpClass(cls):
        cls._media = tempfile.mkdtemp(prefix='adb-galeria-')
        cls._override = override_settings(MEDIA_ROOT=cls._media)
        cls._override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._override.disable()
        shutil.rmtree(cls._media, ignore_errors=True)


def crear_proyecto(slug='proyecto-prueba', **extra):
    datos = {
        'nombre': f'Proyecto {slug}',
        'slug': slug,
        'servicio': 'pisos',
        'descripcion': 'Descripción de prueba.',
    }
    datos.update(extra)
    return Proyecto.objects.create(**datos)


def crear_foto(proyecto, tipo, orden=0, es_portada=False, descripcion=''):
    foto = FotoProyecto(
        proyecto=proyecto,
        tipo=tipo,
        orden=orden,
        es_portada=es_portada,
        descripcion=descripcion,
    )
    foto.imagen.save(
        f'{proyecto.slug}-{tipo}-{orden}.png',
        imagen_png(),
        save=True,
    )
    return foto


class ModelosProyectoTests(MediaTemporalMixin, TestCase):
    def test_opciones_servicio_devuelve_las_nueve_opciones(self):
        opciones = opciones_servicio()
        self.assertEqual(len(opciones), 9)
        self.assertEqual(
            opciones,
            [(item['slug'], item['nombre']) for item in SERVICIOS],
        )

    def test_el_campo_servicio_usa_las_nueve_opciones(self):
        campo = Proyecto._meta.get_field('servicio')
        self.assertEqual(len(campo.choices), 9)
        self.assertEqual(
            {slug for slug, _ in campo.choices},
            {item['slug'] for item in SERVICIOS},
        )

    def test_foto_portada_prioriza_la_foto_marcada(self):
        proyecto = crear_proyecto()
        crear_foto(proyecto, FotoProyecto.Tipo.DESPUES, orden=0)
        portada = crear_foto(
            proyecto,
            FotoProyecto.Tipo.ANTES,
            orden=1,
            es_portada=True,
        )

        self.assertEqual(proyecto.foto_portada.pk, portada.pk)

    def test_foto_portada_usa_la_primera_foto_de_despues(self):
        proyecto = crear_proyecto()
        crear_foto(proyecto, FotoProyecto.Tipo.PROCESO, orden=0)
        primera = crear_foto(proyecto, FotoProyecto.Tipo.DESPUES, orden=1)
        crear_foto(proyecto, FotoProyecto.Tipo.DESPUES, orden=2)

        self.assertEqual(proyecto.foto_portada.pk, primera.pk)

    def test_foto_portada_usa_la_primera_foto_si_no_hay_despues(self):
        proyecto = crear_proyecto()
        antes = crear_foto(proyecto, FotoProyecto.Tipo.ANTES, orden=0)
        crear_foto(proyecto, FotoProyecto.Tipo.PROCESO, orden=1)

        self.assertEqual(proyecto.foto_portada.pk, antes.pk)

    def test_foto_portada_sin_fotos_devuelve_none(self):
        proyecto = crear_proyecto()

        self.assertIsNone(proyecto.foto_portada)

    def test_tiene_antes_y_despues_solo_con_ambos_tipos(self):
        solo_antes = crear_proyecto('solo-antes')
        crear_foto(solo_antes, FotoProyecto.Tipo.ANTES)
        self.assertFalse(solo_antes.tiene_antes_y_despues)

        solo_despues = crear_proyecto('solo-despues')
        crear_foto(solo_despues, FotoProyecto.Tipo.DESPUES)
        self.assertFalse(solo_despues.tiene_antes_y_despues)

        completo = crear_proyecto('completo')
        crear_foto(completo, FotoProyecto.Tipo.ANTES)
        crear_foto(completo, FotoProyecto.Tipo.DESPUES, orden=1)
        self.assertTrue(completo.tiene_antes_y_despues)

    def test_get_absolute_url_apunta_al_detalle(self):
        proyecto = crear_proyecto('mi-proyecto')

        self.assertEqual(proyecto.get_absolute_url(), '/galeria/mi-proyecto/')

    def test_nombre_del_servicio_devuelve_el_nombre_del_catalogo(self):
        proyecto = crear_proyecto(servicio='divisiones-de-bano')

        self.assertEqual(proyecto.nombre_del_servicio, 'Divisiones de baño')

    def test_texto_alternativo_usa_la_descripcion_o_un_texto_de_respaldo(self):
        proyecto = crear_proyecto()

        con_descripcion = crear_foto(
            proyecto,
            FotoProyecto.Tipo.DESPUES,
            descripcion='Cocina terminada',
        )
        self.assertEqual(con_descripcion.texto_alternativo, 'Cocina terminada')

        sin_descripcion = crear_foto(
            proyecto,
            FotoProyecto.Tipo.ANTES,
            orden=1,
        )
        self.assertEqual(
            sin_descripcion.texto_alternativo,
            f'{proyecto.nombre}: antes',
        )


class ComandoProyectosEjemploTests(MediaTemporalMixin, TestCase):
    def ejecutar(self, *argumentos):
        return call_command(
            'cargar_proyectos_ejemplo',
            *argumentos,
            stdout=StringIO(),
        )

    def test_crea_los_seis_proyectos_de_ejemplo(self):
        self.ejecutar()

        self.assertEqual(Proyecto.objects.count(), 6)

    def test_existe_el_proyecto_de_obra_grande(self):
        self.ejecutar()

        self.assertTrue(
            Proyecto.objects.filter(slug='ejemplo-obra-grande').exists()
        )

    def test_el_proyecto_de_obra_grande_esta_marcado(self):
        self.ejecutar()
        proyecto = Proyecto.objects.get(slug='ejemplo-obra-grande')

        self.assertTrue(proyecto.es_obra_grande)

    def test_genera_las_quince_fotografias_marcador(self):
        self.ejecutar()

        self.assertEqual(FotoProyecto.objects.count(), 15)

        obra_grande = Proyecto.objects.get(slug='ejemplo-obra-grande')
        self.assertEqual(len(obra_grande.fotos_antes), 1)
        self.assertEqual(len(obra_grande.fotos_proceso), 3)
        self.assertEqual(len(obra_grande.fotos_despues), 2)

        for foto in FotoProyecto.objects.all():
            self.assertTrue(foto.imagen.name.endswith('.png'))
            self.assertGreater(foto.imagen.size, 0)

    def test_ejecutar_dos_veces_no_duplica(self):
        self.ejecutar()
        self.ejecutar()

        self.assertEqual(Proyecto.objects.count(), 6)
        self.assertEqual(FotoProyecto.objects.count(), 15)


class GaleriaTests(MediaTemporalMixin, TestCase):
    def setUp(self):
        self.publicado = crear_proyecto(
            'cocina-publicada',
            nombre='Cocina publicada',
            servicio='remodelacion',
        )
        self.foto = crear_foto(
            self.publicado,
            FotoProyecto.Tipo.DESPUES,
            descripcion='Cocina terminada',
        )
        self.otro = crear_proyecto(
            'piso-publicado',
            nombre='Piso publicado',
            servicio='pisos',
        )
        crear_foto(
            self.otro,
            FotoProyecto.Tipo.DESPUES,
            descripcion='Piso terminado',
        )
        self.oculto = crear_proyecto(
            'proyecto-oculto',
            nombre='Proyecto oculto',
            publicado=False,
        )
        self.response = self.client.get(reverse('sitio:galeria'))
        self.html = self.response.content.decode()

    def test_la_galeria_responde_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_usa_la_plantilla_de_galeria(self):
        self.assertTemplateUsed(self.response, 'sitio/galeria.html')

    def test_tiene_un_solo_h1(self):
        self.assertEqual(self.html.count('<h1'), 1)
        self.assertContains(self.response, 'Galería de proyectos')

    def test_muestra_los_proyectos_publicados(self):
        self.assertContains(self.response, self.publicado.nombre)
        self.assertContains(self.response, self.otro.nombre)

    def test_muestra_nombres_y_fotografias(self):
        self.assertIn(self.foto.imagen.url, self.html)
        for proyecto in (self.publicado, self.otro):
            self.assertIn(proyecto.nombre, self.html)
            self.assertIn(proyecto.nombre_del_servicio, self.html)

    def test_no_muestra_los_proyectos_no_publicados(self):
        self.assertNotIn(self.oculto.nombre, self.html)

    def test_muestra_mensaje_cuando_no_hay_proyectos(self):
        Proyecto.objects.all().delete()
        response = self.client.get(reverse('sitio:galeria'))

        self.assertContains(response, 'Pronto publicaremos nuestros proyectos.')

    def test_las_tarjetas_enlazan_al_detalle(self):
        self.assertIn(self.publicado.get_absolute_url(), self.html)
        self.assertIn(self.otro.get_absolute_url(), self.html)

    def test_el_detalle_de_un_proyecto_publicado_responde_200(self):
        response = self.client.get(self.publicado.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sitio/proyecto_detalle.html')
        self.assertContains(response, self.publicado.nombre)

    def test_un_slug_inexistente_responde_404(self):
        response = self.client.get('/galeria/no-existe/')

        self.assertEqual(response.status_code, 404)

    def test_un_proyecto_no_publicado_responde_404(self):
        response = self.client.get(self.oculto.get_absolute_url())

        self.assertEqual(response.status_code, 404)


class AntesYDespuesTests(MediaTemporalMixin, TestCase):
    def setUp(self):
        self.comparado = crear_proyecto(
            'proyecto-comparado',
            nombre='Proyecto comparado',
        )
        self.antes = crear_foto(
            self.comparado,
            FotoProyecto.Tipo.ANTES,
            descripcion='Antes de la obra',
        )
        self.despues = crear_foto(
            self.comparado,
            FotoProyecto.Tipo.DESPUES,
            orden=1,
            descripcion='Después de la obra',
        )
        self.solo_despues = crear_proyecto(
            'solo-despues',
            nombre='Solo después',
        )
        self.foto_solo_despues = crear_foto(
            self.solo_despues,
            FotoProyecto.Tipo.DESPUES,
            descripcion='Resultado final',
        )

    def obtener_galeria(self):
        response = self.client.get(reverse('sitio:galeria'))
        return response, response.content.decode()

    def obtener_comparacion(self):
        response, html = self.obtener_galeria()
        return response, html[html.index('comparacion-titulo'):]

    def test_el_proyecto_con_antes_y_despues_aparece_en_el_comparativo(self):
        _, comparacion = self.obtener_comparacion()

        self.assertIn(self.comparado.nombre, comparacion)

    def test_muestra_las_etiquetas_antes_y_despues(self):
        _, comparacion = self.obtener_comparacion()

        self.assertIn('<figcaption>Antes</figcaption>', comparacion)
        self.assertIn('<figcaption>Después</figcaption>', comparacion)

    def test_muestra_las_dos_fotografias_del_comparativo(self):
        _, comparacion = self.obtener_comparacion()

        self.assertIn(self.antes.imagen.url, comparacion)
        self.assertIn(self.despues.imagen.url, comparacion)

    def test_un_proyecto_sin_fotos_de_antes_no_aparece(self):
        response, comparacion = self.obtener_comparacion()

        self.assertNotIn(self.solo_despues.nombre, comparacion)
        self.assertContains(response, self.solo_despues.nombre)

    def test_sin_proyectos_comparables_no_se_muestra_la_seccion(self):
        FotoProyecto.objects.filter(proyecto=self.comparado).delete()
        _, html = self.obtener_galeria()

        self.assertNotIn('comparacion-titulo', html)
