import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

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
