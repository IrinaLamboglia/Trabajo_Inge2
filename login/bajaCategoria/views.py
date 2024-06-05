
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from core.models import Categoria, Publicacion
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

#def bajar_categoria(request, categoria_id):
#    print(categoria_id)
#    categoria = get_object_or_404(Categoria, pk=categoria_id)
#    if request.method == 'POST':
#        # Establecer el estado de todos los publicacions de esta categoría en False
#        publicaciones = Publicacion.objects.filter(categoria = categoria_id)
#        for publicacion in publicaciones:
#            publicacion.estadoCategoria = False
#            publicacion.categoria = None
#            publicacion.save()
        
        # Eliminar la categoría
#        categoria.delete()
        
#        messages.success(request, f'Baja Exitosa.')
#        return redirect('mostarCategoria')
        
#    return render(request, 'bajaCategoria/confirmacionBaja.html', {'categoria': categoria})


def desactivar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    categorias_activas = Categoria.objects.filter(estado=True).count()
    
    if request.method == 'POST':
        print("entra")
        nuevo_estado = not categoria.estado

        if not nuevo_estado and categorias_activas <= 1:
            messages.error(request, 'Debe haber al menos una categoría activa.')
        else:
            categoria.estado = nuevo_estado
            categoria.save()

            # Establecer el estado de todas las publicaciones de esta categoría
            publicaciones = Publicacion.objects.filter(categoria=categoria)
            for publicacion in publicaciones:
                publicacion.estadoCategoria = nuevo_estado
                publicacion.save()

                # Enviar correo al propietario del producto si la categoría se desactiva
                if not nuevo_estado:
                    enviar_correo_desactivacion(publicacion.usuario, categoria, publicacion)
                else:  # Si la categoría se activa nuevamente, enviar correo de activación
                    enviar_correo_activacion(publicacion.usuario, categoria, publicacion)

            mensaje = 'activada' if nuevo_estado else 'desactivada'
            messages.success(request, f'Categoría {mensaje} exitosamente.')
        return redirect('mostarCategoria')

    return render(request, 'bajaCategoria/confirmacion.html', {'categoria': categoria})

def enviar_correo_desactivacion(usuario, categoria, publicacion):
    asunto = "Su producto ha sido desactivado"
    mensaje = (
        f"¡Hola {usuario.nombre} {usuario.apellido}!\n\n"
        f"Su producto '{publicacion.titulo}' ha sido desactivado porque la categoría "
        f"'{categoria.nombre}' ha sido desactivada."
    )
    correo_destino = usuario.email
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [correo_destino])

def enviar_correo_activacion(usuario, categoria, publicacion):
    asunto = "Su producto ha sido activado"
    mensaje = (
        f"¡Hola {usuario.nombre} {usuario.apellido}!\n\n"
        f"Su producto '{publicacion.titulo}' ha sido activado porque la categoría "
        f"'{categoria.nombre}' ha sido activada nuevamente."
    )
    correo_destino = usuario.email
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [correo_destino])

# Asegúrate de que 'settings.DEFAULT_FROM_EMAIL' esté correctamente configurado en settings.py
