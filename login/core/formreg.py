from datetime import date
from django import forms
from . models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'email',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'dni',
            'telefono',
            'contraseña',
            'filial_nombre',
        ]


    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data['email']  # Establecer el correo electrónico como nombre de usuario
        usuario.puntuacion = 3  # Establecer la puntuación predeterminada
        if commit:
            usuario.save()
        return usuario
    
    def clean_filial(self):
        filial = self.cleaned_data['filial']
        if Usuario.objects.filter(filial=filial).exists():
            raise forms.ValidationError("Ya existe un usuario registrado en esta filial.")
        return filial
    
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if len(telefono) >= 10:
            raise forms.ValidationError("El número de teléfono debe tener menos de 10 caracteres.")
        return telefono
