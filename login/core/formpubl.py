from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'descripcion','nuevo', 'categoria', 'imagen']

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        if not imagen:
            raise forms.ValidationError("Por favor, sube una imagen.")
        return imagen
