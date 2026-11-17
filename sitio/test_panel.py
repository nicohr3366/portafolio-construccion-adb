import shutil
import tempfile
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import NoReverseMatch, reverse
from PIL import Image

from .models import FotoProyecto, Proyecto

# Carpeta temporal para las fotos que suben las pruebas; se borra al terminar.
MEDIA_TEMPORAL = tempfile.mkdtemp(prefix='adb-panel-')

# Contraseña inventada solo para las pruebas: vive en la base de datos temporal
# de las pruebas y no corresponde a ningún usuario real.
CLAVE_DE_PRUEBA = 'clave-inventada-solo-para-pruebas'

PANEL = '/panel/'
LOGIN = '/panel/login/'
ALTA_PROYECTO = '/panel/sitio/proyecto/add/'


@override_settings(
    MEDIA_ROOT=MEDIA_TEMPORAL,
    # Hash rápido solo para las pruebas: con el real cada prueba tarda segundos.
    PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'],
)
class PanelTestCase(TestCase):
    """Base de las pruebas del panel: fotos en una carpeta temporal."""

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def crear_propietario(self):
        return get_user_model().objects.create_superuser(
            username='propietario-de-prueba',
            email='propietario@example.com',
            password=CLAVE_DE_PRUEBA,
        )


class InicioDeSesionPanelTests(PanelTestCase):
    """HU-24 · Iniciar sesión en el panel."""

    def test_panel_sin_sesion_redirige_al_inicio_de_sesion(self):
        response = self.client.get(PANEL)

        self.assertRedirects(
            response,
            f'{LOGIN}?next={PANEL}',
            fetch_redirect_response=False,
        )

    def test_pagina_interna_sin_sesion_redirige_al_inicio_de_sesion(self):
        response = self.client.get(ALTA_PROYECTO)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['Location'],
            f'{LOGIN}?next={ALTA_PROYECTO}',
        )

    def test_contrasena_incorrecta_no_entra(self):
        propietario = self.crear_propietario()

        response = self.client.post(LOGIN, {
            'username': propietario.username,
            'password': 'contrasena-equivocada',
            'next': PANEL,
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertContains(response, 'errornote')
        self.assertEqual(self.client.get(PANEL).status_code, 302)

    def test_usuario_sin_permiso_de_personal_no_entra(self):
        visitante = get_user_model().objects.create_user(
            username='visitante-de-prueba',
            password=CLAVE_DE_PRUEBA,
        )

        response = self.client.post(LOGIN, {
            'username': visitante.username,
            'password': CLAVE_DE_PRUEBA,
            'next': PANEL,
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(self.client.get(PANEL).status_code, 302)

    def test_usuario_sin_permiso_de_personal_con_sesion_no_ve_el_panel(self):
        visitante = get_user_model().objects.create_user(
            username='visitante-de-prueba',
            password=CLAVE_DE_PRUEBA,
        )
        self.client.force_login(visitante)

        self.assertEqual(self.client.get(PANEL).status_code, 302)
        self.assertEqual(self.client.get(ALTA_PROYECTO).status_code, 302)

    def test_el_propietario_entra_y_ve_el_panel(self):
        propietario = self.crear_propietario()

        response = self.client.post(LOGIN, {
            'username': propietario.username,
            'password': CLAVE_DE_PRUEBA,
            'next': PANEL,
        })
        self.assertRedirects(response, PANEL, fetch_redirect_response=False)

        response = self.client.get(PANEL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Panel de administración – Alexander Drada')
        self.assertContains(response, 'Contenido del sitio')

    def test_la_direccion_admin_ya_no_existe(self):
        self.assertEqual(self.client.get('/admin/').status_code, 404)
        self.assertEqual(self.client.get('/admin/login/').status_code, 404)

    def test_el_menu_publico_no_enlaza_al_panel(self):
        html = self.client.get('/').content.decode()

        self.assertNotIn('/panel', html)
        self.assertNotIn('/admin', html)


def foto(nombre='foto.png', formato='PNG', tipo_mime='image/png'):
    """Foto de 12×8 píxeles lista para subir en un formulario."""
    buffer = BytesIO()
    Image.new('RGB', (12, 8), (120, 120, 120)).save(buffer, format=formato)
    return SimpleUploadedFile(nombre, buffer.getvalue(), content_type=tipo_mime)


def datos_de_alta(**cambios):
    """Datos del formulario de alta: un proyecto con una foto «antes» y una
    «después» (la tercera fila del inline queda vacía)."""
    datos = {
        'nombre': 'Obra de prueba',
        'slug': 'obra-de-prueba',
        'servicio': 'pintura',
        'descripcion': 'Descripción de prueba',
        'fotos-TOTAL_FORMS': '3',
        'fotos-INITIAL_FORMS': '0',
        'fotos-MIN_NUM_FORMS': '1',
        'fotos-MAX_NUM_FORMS': '1000',
        'fotos-0-imagen': foto('antes.png'),
        'fotos-0-tipo': 'antes',
        'fotos-0-orden': '1',
        'fotos-0-descripcion': '',
        'fotos-1-imagen': foto('despues.png'),
        'fotos-1-tipo': 'despues',
        'fotos-1-orden': '2',
        'fotos-1-descripcion': '',
        'fotos-2-tipo': 'despues',
        'fotos-2-orden': '0',
        'fotos-2-descripcion': '',
    }
    datos.update(cambios)
    return datos


def sin_fotos(datos):
    """Quita las dos fotos subidas, como si no se hubiera escogido ninguna."""
    datos.pop('fotos-0-imagen')
    datos.pop('fotos-1-imagen')
    return datos


class PanelConSesionTestCase(PanelTestCase):
    def setUp(self):
        self.client.force_login(self.crear_propietario())
        self.url_alta = reverse('admin:sitio_proyecto_add')

    def enviar_alta(self, datos):
        return self.client.post(self.url_alta, datos)


class AgregarProyectoTests(PanelConSesionTestCase):
    """HU-25 · Agregar proyecto."""

    def test_el_formulario_de_alta_responde_200(self):
        response = self.client.get(self.url_alta)

        self.assertEqual(response.status_code, 200)

    def test_el_formulario_pide_nombre_descripcion_y_fotos(self):
        response = self.client.get(self.url_alta)

        formulario = response.context['adminform'].form
        self.assertEqual(
            list(formulario.fields),
            ['nombre', 'slug', 'servicio', 'descripcion', 'es_obra_grande'],
        )
        formset = response.context['inline_admin_formsets'][0].formset
        self.assertEqual(formset.min_num, 1)
        # Después de estos cinco, Django agrega sus campos internos (id, etc.).
        self.assertEqual(
            list(formset.empty_form.fields)[:5],
            ['imagen', 'tipo', 'descripcion', 'es_portada', 'orden'],
        )

    def test_el_formulario_no_muestra_publicado_ni_destacado(self):
        response = self.client.get(self.url_alta)

        self.assertNotContains(response, 'name="publicado"')
        self.assertNotContains(response, 'name="destacado"')

    def test_la_direccion_web_se_llena_sola_desde_el_nombre(self):
        response = self.client.get(self.url_alta)

        self.assertContains(response, 'data-prepopulated-fields')
        self.assertContains(response, '#id_nombre')
        self.assertContains(response, '#id_slug')

    def test_las_fotos_solo_se_manejan_dentro_del_proyecto(self):
        response = self.client.get(PANEL)

        self.assertContains(response, reverse('admin:sitio_proyecto_changelist'))
        with self.assertRaises(NoReverseMatch):
            reverse('admin:sitio_fotoproyecto_changelist')
        self.assertEqual(
            self.client.get('/panel/sitio/fotoproyecto/').status_code,
            404,
        )

    def test_crear_un_proyecto_con_dos_fotos(self):
        response = self.enviar_alta(datos_de_alta())

        self.assertRedirects(
            response,
            reverse('admin:sitio_proyecto_changelist'),
            fetch_redirect_response=False,
        )
        self.assertEqual(Proyecto.objects.count(), 1)
        proyecto = Proyecto.objects.get()
        self.assertEqual(proyecto.nombre, 'Obra de prueba')
        self.assertEqual(proyecto.slug, 'obra-de-prueba')
        self.assertEqual(proyecto.descripcion, 'Descripción de prueba')
        self.assertEqual(proyecto.fotos.count(), 2)
        self.assertEqual(
            sorted(proyecto.fotos.values_list('tipo', flat=True)),
            ['antes', 'despues'],
        )

    def test_el_proyecto_nuevo_nace_publicado_y_no_destacado(self):
        self.enviar_alta(datos_de_alta())
        proyecto = Proyecto.objects.get()

        self.assertTrue(proyecto.publicado)
        self.assertFalse(proyecto.destacado)
        self.assertFalse(proyecto.es_obra_grande)

    def test_obra_de_gran_escala_se_marca_con_on(self):
        self.enviar_alta(datos_de_alta(es_obra_grande='on'))

        self.assertTrue(Proyecto.objects.get().es_obra_grande)

    def test_el_proyecto_nuevo_aparece_en_la_galeria(self):
        self.enviar_alta(datos_de_alta())

        response = self.client.get(reverse('sitio:galeria'))

        self.assertContains(response, 'Obra de prueba')
        self.assertContains(response, Proyecto.objects.get().get_absolute_url())

    def test_el_proyecto_tiene_boton_ver_en_el_sitio(self):
        self.enviar_alta(datos_de_alta())
        proyecto = Proyecto.objects.get()

        response = self.client.get(
            reverse('admin:sitio_proyecto_change', args=[proyecto.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ver en el sitio')

    def test_sin_fotos_no_se_guarda(self):
        response = self.enviar_alta(sin_fotos(datos_de_alta()))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Proyecto.objects.count(), 0)
        self.assertEqual(FotoProyecto.objects.count(), 0)

    def test_sin_ninguna_fila_de_fotos_se_pide_al_menos_una(self):
        datos = sin_fotos(datos_de_alta())
        datos['fotos-TOTAL_FORMS'] = '0'

        response = self.enviar_alta(datos)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El proyecto debe tener al menos una foto.')
        self.assertEqual(Proyecto.objects.count(), 0)

    def test_sin_nombre_no_se_guarda(self):
        response = self.enviar_alta(datos_de_alta(nombre=''))

        self.assertEqual(response.status_code, 200)
        self.assertIn('nombre', response.context['adminform'].form.errors)
        self.assertEqual(Proyecto.objects.count(), 0)

    def test_sin_descripcion_no_se_guarda(self):
        response = self.enviar_alta(datos_de_alta(descripcion=''))

        self.assertEqual(response.status_code, 200)
        self.assertIn('descripcion', response.context['adminform'].form.errors)
        self.assertEqual(Proyecto.objects.count(), 0)
        self.assertEqual(FotoProyecto.objects.count(), 0)

    def test_sin_servicio_no_se_guarda(self):
        response = self.enviar_alta(datos_de_alta(servicio=''))

        self.assertEqual(response.status_code, 200)
        self.assertIn('servicio', response.context['adminform'].form.errors)
        self.assertEqual(Proyecto.objects.count(), 0)

    def test_una_foto_gif_no_se_guarda(self):
        datos = datos_de_alta(**{
            'fotos-1-imagen': foto('animacion.gif', 'GIF', 'image/gif'),
        })

        response = self.enviar_alta(datos)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Solo se permiten fotos JPG, PNG o WEBP.')
        self.assertEqual(Proyecto.objects.count(), 0)
        self.assertEqual(FotoProyecto.objects.count(), 0)

    def test_un_archivo_txt_como_foto_no_se_guarda(self):
        datos = datos_de_alta(**{
            'fotos-1-imagen': SimpleUploadedFile(
                'notas.txt',
                'esto no es una foto'.encode(),
                content_type='text/plain',
            ),
        })

        response = self.enviar_alta(datos)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Proyecto.objects.count(), 0)
        self.assertEqual(FotoProyecto.objects.count(), 0)

    def test_una_foto_de_mas_de_5_mb_no_se_guarda(self):
        original = foto('pesada.png')
        relleno = b'\0' * (5 * 1024 * 1024 + 1)
        pesada = SimpleUploadedFile(
            'pesada.png',
            original.read() + relleno,
            content_type='image/png',
        )

        response = self.enviar_alta(datos_de_alta(**{'fotos-1-imagen': pesada}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'La foto pesa más de 5 MB.')
        self.assertEqual(Proyecto.objects.count(), 0)

    def test_se_aceptan_fotos_jpg_y_webp(self):
        datos = datos_de_alta(**{
            'fotos-0-imagen': foto('uno.jpg', 'JPEG', 'image/jpeg'),
            'fotos-1-imagen': foto('dos.webp', 'WEBP', 'image/webp'),
        })

        self.enviar_alta(datos)

        self.assertEqual(Proyecto.objects.get().fotos.count(), 2)

    def test_dos_fotos_principales_no_se_guardan(self):
        datos = datos_de_alta(**{
            'fotos-0-es_portada': 'on',
            'fotos-1-es_portada': 'on',
        })

        response = self.enviar_alta(datos)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marca solo una foto como foto principal.')
        self.assertEqual(Proyecto.objects.count(), 0)
        self.assertEqual(FotoProyecto.objects.count(), 0)

    def test_una_sola_foto_principal_si_se_guarda(self):
        self.enviar_alta(datos_de_alta(**{'fotos-1-es_portada': 'on'}))

        proyecto = Proyecto.objects.get()
        self.assertEqual(proyecto.fotos.filter(es_portada=True).count(), 1)
        self.assertEqual(proyecto.foto_portada.tipo, 'despues')

    def test_la_direccion_web_no_se_puede_repetir(self):
        self.enviar_alta(datos_de_alta())

        response = self.enviar_alta(datos_de_alta(nombre='Otra obra'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('slug', response.context['adminform'].form.errors)
        self.assertEqual(Proyecto.objects.count(), 1)
