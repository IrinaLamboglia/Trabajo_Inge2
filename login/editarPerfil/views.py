from django.shortcuts import render, redirect
from core.models import Usuario

from django.shortcuts import render, redirect
from core.models import Usuario
from django.contrib import messages

def editar_ayudante(request, id):
    
    ayudante = Usuario.objects.get(id=id)
    

    if request.method == 'POST':
        nuevo_email = request.POST.get('nuevo_email')
        nuevo_nombre = request.POST.get('nuevo_nombre')
        nuevo_apellido = request.POST.get('nuevo_apellido')
        nueva_filial = request.POST.get('nueva_filial')
        nuevo_dni = request.POST.get('nuevo_dni')
        nueva_fecha_nacimiento = request.POST.get('nueva_fecha_nacimiento')
        nuevo_telefono = request.POST.get('nuevo_telefono')
        nueva_contrasena = request.POST.get('nueva_contrasena')

        # Verificar si el nuevo correo electrónico corresponde a un usuario ya registrado
        if Usuario.objects.exclude(id=id).filter(email=nuevo_email).exists():
            messages.error(request, 'El correo electrónico ya corresponde a un usuario registrado.')
            return redirect('editar_ayudante',id=id)
        else:
            #verifico que la contraseña tenga al menos 6 digitos
            if nueva_contrasena and nueva_contrasena != ayudante.contraseña and len(nueva_contrasena) < 6:
                messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
                return redirect('editar_ayudante', id=id)
            #verifico que la filial no este repetida 
            else:
                if Usuario.objects.exclude(id=id).filter(filial=nueva_filial).exists():
                    messages.error(request, 'Esa filial ya esta registrado con un ayudante')
                    return redirect('editar_ayudante', id=id)
                else:
                    # Actualizar la información del ayudante
                    ayudante.email = nuevo_email
                    ayudante.nombre = nuevo_nombre
                    ayudante.apellido = nuevo_apellido
                    ayudante.filial = nueva_filial
                    ayudante.dni = nuevo_dni
                    ayudante.fecha_nacimiento = nueva_fecha_nacimiento
                    ayudante.telefono = nuevo_telefono
                    ayudante.contraseña = nueva_contrasena
                    ayudante.save()
                    return redirect('home')
        
    return render(request, 'admin/editar_ayudante.html', {'ayudante': ayudante})
