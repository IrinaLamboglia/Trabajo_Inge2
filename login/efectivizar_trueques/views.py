from django.shortcuts import render, redirect, get_object_or_404
from core.models import Trueque,Solicitud
from django.db.models import Q
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
import datetime

def efectivizar_trueques(request):
    usuario_actual =get_user_model().objects.get(pk=request.user.id)
 # Obtener el usuario actual
    #filial=usuario_actual.filial # Acceder a la filial del usuario desde el modelo
    today = datetime.date.today()

    query = request.GET.get('q')
    if query:
        trueques = Trueque.objects.filter(
            Q(codigo_confirmacion_solicitante=query) | Q(codigo_confirmacion_receptor=query)
        )
        if not trueques.exists():
            messages.error(request, 'No se encontró ningún trueque con el código proporcionado.')
    else:
        trueques = Trueque.objects.filter(aceptado=False, confirmado=True) #filial=filial, turno=today
    return render(request, 'efectivizar_trueque/efectivizar_trueque.html', {'trueques': trueques})

def enviar_correo_ayudante(ayudante):
    asunto = "No olvides de calificar el producto"
    mensaje = f"¡Hola {ayudante.nombre} {ayudante.apellido}! Recuerda califica el producto una vez terminado el trueque, Saludos."
    correo_destino = ayudante.email
    send_mail(asunto, mensaje, 'tucorreo@gmail.com', [correo_destino])

def aceptacion_trueque(request, id):
    print("estoty")
    trueque = Trueque.objects.get(id=id)
    trueque.aceptado = True
    trueque.fecha_aceptacion = timezone.now() 
     # Asigna la fecha y hora actual
    trueque.save()
    enviar_correo_ayudante(trueque.solicitante)
    enviar_correo_ayudante(trueque.receptor)


    return redirect('efectivizar_trueque')



def rechazar_efectivizacion(request, id):
    trueque = get_object_or_404(Trueque, id=id)
    solicitud = Solicitud.objects.filter(publicacion=trueque.solicitante, publicacionOfrecida=trueque.receptor).first()
    
    if solicitud:
        # Reactivar las publicaciones
        solicitud.publicacion.trueque = False
        solicitud.publicacionOfrecida.estado = False
        solicitud.publicacion.save()
        solicitud.publicacionOfrecida.save()

        # Eliminar la solicitud
        solicitud.delete()

    # Eliminar el trueque
    trueque.delete()

    messages.success(request, 'El trueque ha sido rechazado y las publicaciones reactivadas.')
    return redirect('efectivizar_trueques')


# views.py
def penalizar_trueque(request, trueque_id):
    if request.method == 'POST':
        # Obtener el trueque a penalizar
        trueque = get_object_or_404(Trueque, id=trueque_id)

        # Penalizar al usuario asociado al trueque
        usuario = trueque.solicitante  # Obtener el usuario solicitante del trueque
        usuario.puntuacion -= 1
        usuario.save()

        # Manejar la solicitud (reactivar publicaciones y eliminar solicitud)
        solicitud = Solicitud.objects.filter(solicitante=trueque.solicitante, publicacionOfrecida__usuario=trueque.receptor).first()
        if solicitud:
            solicitud.publicacion.trueque = False
            solicitud.publicacionOfrecida.estado = False
            solicitud.publicacion.save()
            solicitud.publicacionOfrecida.save()
            solicitud.delete()

        # Eliminar el trueque
        trueque.delete()

        # Mensaje de éxito
        messages.success(request, 'El usuario ha sido penalizado y las publicaciones reactivadas.')

    # Redireccionar a la página de efectivizar_trueques independientemente del método de solicitud
    return redirect('efectivizar_trueque')
