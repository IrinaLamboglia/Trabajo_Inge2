from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Usuario, Filial
def editar_ayudante(request, id):
    ayudante = get_object_or_404(Usuario, id=id)

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
        elif nueva_contrasena and nueva_contrasena != ayudante.contraseña and len(nueva_contrasena) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
        elif not Filial.objects.filter(nombre=nueva_filial).exists():
            messages.error(request, 'La filial no está registrada en el sistema.')    
        elif Usuario.objects.exclude(id=id).filter(filial_nombre=nueva_filial).exists():
            messages.error(request, 'Esa filial ya está registrada con un ayudante.')
        else:
            # Verificación de la edad
            birthdate = date.fromisoformat(nueva_fecha_nacimiento)
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            if age < 18:
                messages.error(request, 'El usuario debe tener al menos 18 años.')
            else:
                # Actualizar la información del ayudante
                ayudante.email = nuevo_email
                ayudante.nombre = nuevo_nombre
                ayudante.apellido = nuevo_apellido
                ayudante.filial_nombre = nueva_filial
                ayudante.dni = nuevo_dni
                ayudante.fecha_nacimiento = nueva_fecha_nacimiento
                ayudante.telefono = nuevo_telefono
                ayudante.contraseña = nueva_contrasena
                ayudante.save()
                messages.success(request, 'Información del ayudante actualizada correctamente.')
                return redirect('home')
        
    return render(request, 'admin/editar_ayudante.html', {'ayudante': ayudante})