from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms.models import BaseInlineFormSet

from .models import FotoProyecto

EXTENSIONES_PERMITIDAS = ['jpg', 'jpeg', 'png', 'webp']
TAMANO_MAXIMO_MB = 5


class FotoProyectoForm(forms.ModelForm):
    class Meta:
        model = FotoProyecto
        fields = ['imagen', 'tipo', 'descripcion', 'es_portada', 'orden']

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if not imagen:
            return imagen
        FileExtensionValidator(
            allowed_extensions=EXTENSIONES_PERMITIDAS,
            message='Solo se permiten fotos JPG, PNG o WEBP.',
        )(imagen)
        if imagen.size > TAMANO_MAXIMO_MB * 1024 * 1024:
            raise ValidationError(f'La foto pesa más de {TAMANO_MAXIMO_MB} MB.')
        return imagen


class FotosRequeridasFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        fotos = 0
        portadas = 0
        for form in self.forms:
            datos = getattr(form, 'cleaned_data', None) or {}
            if not datos or datos.get('DELETE'):
                continue
            if datos.get('imagen'):
                fotos += 1
                if datos.get('es_portada'):
                    portadas += 1
        if fotos == 0:
            raise ValidationError('El proyecto debe tener al menos una foto.')
        if portadas > 1:
            raise ValidationError('Marca solo una foto como foto principal.')
