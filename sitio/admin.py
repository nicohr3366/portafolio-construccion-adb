from django.contrib import admin
from django.utils.html import format_html

from .forms import FotoProyectoForm, FotosRequeridasFormSet
from .models import FotoProyecto, Proyecto

admin.site.site_header = 'Panel de administración – Alexander Drada'
admin.site.site_title = 'Panel Alexander Drada'
admin.site.index_title = 'Contenido del sitio'
admin.site.site_url = '/'


class FotoProyectoInline(admin.TabularInline):
    model = FotoProyecto
    form = FotoProyectoForm
    formset = FotosRequeridasFormSet
    fields = ['vista_previa', 'imagen', 'tipo', 'descripcion', 'es_portada', 'orden']
    readonly_fields = ['vista_previa']
    extra = 3
    min_num = 1

    @admin.display(description='Vista previa')
    def vista_previa(self, foto):
        if foto.pk and foto.imagen:
            return format_html(
                '<img src="{}" alt="" style="max-height:80px;max-width:120px;">',
                foto.imagen.url,
            )
        return '—'


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    fields = ['nombre', 'slug', 'servicio', 'descripcion', 'es_obra_grande']
    prepopulated_fields = {'slug': ['nombre']}
    inlines = [FotoProyectoInline]
    # El servicio se agrega a la lista y a los filtros en HU-30.
    list_display = ['nombre', 'es_obra_grande', 'numero_de_fotos', 'creado']
    list_filter = ['es_obra_grande']
    search_fields = ['nombre', 'descripcion']

    @admin.display(description='Fotos')
    def numero_de_fotos(self, proyecto):
        return proyecto.fotos.count()
