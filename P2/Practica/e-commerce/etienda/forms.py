from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_uppercase_start(value):
    if not value[0].isupper():
        raise ValidationError(
            _("El nombre no empieza por mayuscula"),
        )
class ProductoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100, validators=[validate_uppercase_start])
    precio = forms.DecimalField(label='Precio')
    descripcion = forms.CharField(label='Descripción', widget=forms.Textarea)
    categoria = forms.CharField(label='Categoría', max_length=50)
    imagen = forms.ImageField(label='Imagen', required=False)
