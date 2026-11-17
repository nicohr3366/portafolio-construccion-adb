from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont

from sitio.catalogo import opciones_servicio
from sitio.models import FotoProyecto, Proyecto

ANCHO = 1200
ALTO = 800

# Colores de las fotografías marcador, uno por tipo de foto.
COLORES = {
    FotoProyecto.Tipo.ANTES: (156, 163, 175),
    FotoProyecto.Tipo.PROCESO: (180, 140, 90),
    FotoProyecto.Tipo.DESPUES: (43, 58, 74),
}

COLORES_TEXTO = {
    FotoProyecto.Tipo.ANTES: (31, 41, 51),
    FotoProyecto.Tipo.PROCESO: (31, 41, 51),
    FotoProyecto.Tipo.DESPUES: (255, 255, 255),
}

COLORES_BORDE = {
    FotoProyecto.Tipo.ANTES: (82, 96, 109),
    FotoProyecto.Tipo.PROCESO: (255, 255, 255),
    FotoProyecto.Tipo.DESPUES: (255, 255, 255),
}

PROYECTOS = [
    {
        'slug': 'ejemplo-remodelacion-cocina',
        'nombre': 'Remodelación de cocina (ejemplo)',
        'servicio': 'remodelacion',
        'descripcion': (
            'Proyecto de ejemplo: renovación de una cocina en una vivienda. '
            'Se cambiaron los acabados y la distribución del espacio. '
            'Las fotografías son marcadores provisionales.'
        ),
        'es_obra_grande': False,
        'fotos': [
            (FotoProyecto.Tipo.ANTES, 'Cocina antes de la remodelación (ejemplo)'),
            (FotoProyecto.Tipo.DESPUES, 'Cocina terminada (ejemplo)'),
        ],
    },
    {
        'slug': 'ejemplo-casa-dos-pisos',
        'nombre': 'Casa de dos pisos (ejemplo)',
        'servicio': 'construccion-desde-cero',
        'descripcion': (
            'Proyecto de ejemplo: construcción de una vivienda de dos pisos. '
            'Se muestra el avance de la obra y el resultado final. '
            'Las fotografías son marcadores provisionales.'
        ),
        'es_obra_grande': False,
        'fotos': [
            (FotoProyecto.Tipo.PROCESO, 'Avance de la obra (ejemplo)'),
            (FotoProyecto.Tipo.DESPUES, 'Casa terminada (ejemplo)'),
        ],
    },
    {
        'slug': 'ejemplo-piso-porcelanato',
        'nombre': 'Piso en porcelanato (ejemplo)',
        'servicio': 'pisos',
        'descripcion': (
            'Proyecto de ejemplo: instalación de piso en porcelanato en un '
            'espacio interior. Las fotografías son marcadores provisionales.'
        ),
        'es_obra_grande': False,
        'fotos': [
            (FotoProyecto.Tipo.ANTES, 'Espacio antes de instalar el piso (ejemplo)'),
            (FotoProyecto.Tipo.DESPUES, 'Piso instalado (ejemplo)'),
        ],
    },
    {
        'slug': 'ejemplo-estuco-pintura-fachada',
        'nombre': 'Estuco y pintura de fachada (ejemplo)',
        'servicio': 'pintura',
        'descripcion': (
            'Proyecto de ejemplo: preparación de la fachada con estuco y '
            'pintura exterior. Las fotografías son marcadores provisionales.'
        ),
        'es_obra_grande': False,
        'fotos': [
            (FotoProyecto.Tipo.ANTES, 'Fachada antes del estuco (ejemplo)'),
            (FotoProyecto.Tipo.DESPUES, 'Fachada pintada (ejemplo)'),
        ],
    },
    {
        'slug': 'ejemplo-division-bano',
        'nombre': 'División de baño en vidrio (ejemplo)',
        'servicio': 'divisiones-de-bano',
        'descripcion': (
            'Proyecto de ejemplo: instalación de una división de baño a la '
            'medida del espacio. Las fotografías son marcadores provisionales.'
        ),
        'es_obra_grande': False,
        'fotos': [
            (FotoProyecto.Tipo.DESPUES, 'División de baño instalada (ejemplo)'),
        ],
    },
    {
        'slug': 'ejemplo-obra-grande',
        'nombre': 'Obra grande institucional (ejemplo)',
        'servicio': 'construccion-desde-cero',
        'descripcion': (
            'Proyecto de ejemplo de una obra de gran escala. Muestra '
            'fotografías de antes, del proceso de obra y del resultado final. '
            'Las fotografías son marcadores provisionales.'
        ),
        'es_obra_grande': True,
        'fotos': [
            (FotoProyecto.Tipo.ANTES, 'Obra antes de iniciar (ejemplo)'),
            (FotoProyecto.Tipo.PROCESO, 'Proceso de obra, etapa 1 (ejemplo)'),
            (FotoProyecto.Tipo.PROCESO, 'Proceso de obra, etapa 2 (ejemplo)'),
            (FotoProyecto.Tipo.PROCESO, 'Proceso de obra, etapa 3 (ejemplo)'),
            (FotoProyecto.Tipo.DESPUES, 'Resultado final (ejemplo)'),
            (FotoProyecto.Tipo.DESPUES, 'Resultado final, vista general (ejemplo)'),
        ],
    },
]


def _fuente(tamano):
    try:
        return ImageFont.load_default(size=tamano)
    except TypeError:
        return ImageFont.load_default()


def _fuente_ajustada(dibujo, texto, tamano, maximo):
    while tamano > 16:
        fuente = _fuente(tamano)
        if dibujo.textlength(texto, font=fuente) <= maximo:
            return fuente
        tamano -= 2
    return _fuente(tamano)


def _imagen_marcador(tipo, descripcion):
    imagen = Image.new('RGB', (ANCHO, ALTO), COLORES[tipo])
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle(
        (12, 12, ANCHO - 13, ALTO - 13),
        outline=COLORES_BORDE[tipo],
        width=8,
    )

    etiqueta = FotoProyecto.Tipo(tipo).label
    color = COLORES_TEXTO[tipo]
    lineas = [
        ('Imagen de ejemplo', 72),
        (f'{etiqueta} · {descripcion}', 44),
    ]
    alto_linea = 92
    y = ALTO // 2 - (alto_linea * len(lineas)) // 2 + alto_linea // 2

    for texto, tamano in lineas:
        fuente = _fuente_ajustada(dibujo, texto, tamano, ANCHO - 120)
        dibujo.text(
            (ANCHO // 2, y),
            texto,
            fill=color,
            font=fuente,
            anchor='mm',
        )
        y += alto_linea

    return imagen


def _archivo_png(imagen):
    buffer = BytesIO()
    imagen.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = 'Carga seis proyectos de ejemplo con fotografías marcador.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reiniciar',
            action='store_true',
            help='Elimina y vuelve a crear solo los proyectos de ejemplo.',
        )

    def handle(self, *args, **opciones):
        slugs_validos = {slug for slug, _ in opciones_servicio()}
        for datos in PROYECTOS:
            if datos['servicio'] not in slugs_validos:
                raise CommandError(
                    f'El servicio "{datos["servicio"]}" del proyecto '
                    f'"{datos["slug"]}" no existe en el catálogo.'
                )

        with transaction.atomic():
            if opciones['reiniciar']:
                self._eliminar_ejemplos()

            creados = 0
            for datos in PROYECTOS:
                proyecto, creado = Proyecto.objects.get_or_create(
                    slug=datos['slug'],
                    defaults={
                        'nombre': datos['nombre'],
                        'servicio': datos['servicio'],
                        'descripcion': datos['descripcion'],
                        'es_obra_grande': datos['es_obra_grande'],
                        'publicado': True,
                    },
                )
                if not creado:
                    self.stdout.write(f'Ya existe: {proyecto.nombre}')
                    continue

                self._crear_fotos(proyecto, datos['fotos'])
                creados += 1
                self.stdout.write(f'Creado: {proyecto.nombre}')

        total_fotos = FotoProyecto.objects.filter(
            proyecto__slug__in=[datos['slug'] for datos in PROYECTOS]
        ).count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Proyectos de ejemplo creados en esta ejecución: {creados}. '
                f'Fotografías marcador: {total_fotos}.'
            )
        )

    def _eliminar_ejemplos(self):
        slugs = [datos['slug'] for datos in PROYECTOS]
        proyectos = Proyecto.objects.filter(slug__in=slugs)
        archivos = [
            foto.imagen
            for foto in FotoProyecto.objects.filter(proyecto__in=proyectos)
            if foto.imagen
        ]
        proyectos.delete()
        for archivo in archivos:
            archivo.delete(save=False)
        self.stdout.write(f'Proyectos de ejemplo eliminados: {len(archivos)} fotos.')

    def _crear_fotos(self, proyecto, fotos):
        portada_asignada = False

        for indice, (tipo, descripcion) in enumerate(fotos):
            es_portada = (
                tipo == FotoProyecto.Tipo.DESPUES and not portada_asignada
            )
            foto = FotoProyecto(
                proyecto=proyecto,
                tipo=tipo,
                descripcion=descripcion,
                es_portada=es_portada,
                orden=indice,
            )
            imagen = _imagen_marcador(tipo, descripcion)
            foto.imagen.save(
                f'{tipo}-{indice + 1:02d}.png',
                _archivo_png(imagen),
                save=False,
            )
            foto.save()

            if es_portada:
                portada_asignada = True
