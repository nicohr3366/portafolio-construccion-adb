from django.db import models
from django.urls import reverse

from .catalogo import nombre_servicio, opciones_servicio


def ruta_foto_proyecto(instancia, nombre_archivo):
    return f'proyectos/{instancia.proyecto.slug}/{nombre_archivo}'


class Proyecto(models.Model):
    nombre = models.CharField('nombre', max_length=120)

    slug = models.SlugField(
        'dirección web',
        max_length=140,
        unique=True,
        help_text='Se usa en la dirección de la página del proyecto.',
    )

    servicio = models.CharField(
        'tipo de servicio',
        max_length=40,
        choices=opciones_servicio(),
    )

    descripcion = models.TextField('descripción')

    es_obra_grande = models.BooleanField(
        'obra de gran escala',
        default=False,
        help_text='Marca las obras grandes que muestran proceso y resultado final.',
    )

    publicado = models.BooleanField('publicado', default=True)

    destacado = models.BooleanField(
        'destacado en el inicio',
        default=False
    )

    creado = models.DateTimeField('creado', auto_now_add=True)

    actualizado = models.DateTimeField('actualizado', auto_now=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('sitio:proyecto_detalle', args=[self.slug])

    @property
    def nombre_del_servicio(self):
        return nombre_servicio(self.servicio)

    @property
    def foto_portada(self):
        fotos = list(self.fotos.all())

        for foto in fotos:
            if foto.es_portada:
                return foto

        for foto in fotos:
            if foto.tipo == FotoProyecto.Tipo.DESPUES:
                return foto

        return fotos[0] if fotos else None

    def fotos_de_tipo(self, tipo):
        return [foto for foto in self.fotos.all() if foto.tipo == tipo]

    @property
    def fotos_antes(self):
        return self.fotos_de_tipo(FotoProyecto.Tipo.ANTES)

    @property
    def fotos_proceso(self):
        return self.fotos_de_tipo(FotoProyecto.Tipo.PROCESO)

    @property
    def fotos_despues(self):
        return self.fotos_de_tipo(FotoProyecto.Tipo.DESPUES)

    @property
    def tiene_antes_y_despues(self):
        return bool(self.fotos_antes) and bool(self.fotos_despues)


class FotoProyecto(models.Model):

    class Tipo(models.TextChoices):
        ANTES = 'antes', 'Antes'
        PROCESO = 'proceso', 'Proceso'
        DESPUES = 'despues', 'Después'

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name='fotos',
        verbose_name='proyecto',
    )

    imagen = models.ImageField(
        'imagen',
        upload_to=ruta_foto_proyecto
    )

    tipo = models.CharField(
        'tipo de foto',
        max_length=10,
        choices=Tipo.choices,
        default=Tipo.DESPUES,
    )

    descripcion = models.CharField(
        'descripción corta',
        max_length=150,
        blank=True,
        help_text='Texto alternativo de la foto (lo leen los lectores de pantalla).',
    )

    es_portada = models.BooleanField('foto principal', default=False)

    orden = models.PositiveIntegerField('orden', default=0)

    class Meta:
        ordering = ['orden', 'id']
        verbose_name = 'foto del proyecto'
        verbose_name_plural = 'fotos del proyecto'

    def __str__(self):
        return f'{self.proyecto} – {self.get_tipo_display()}'

    @property
    def texto_alternativo(self):
        return self.descripcion or (
            f'{self.proyecto.nombre}: '
            f'{self.get_tipo_display().lower()}'
        )
