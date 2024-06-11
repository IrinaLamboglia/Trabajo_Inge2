from django.shortcuts import render, redirect, get_object_or_404
from core.models import Trueque,Solicitud,Usuario,Filial,Turno
from django.db.models import Q
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
import datetime
def efectivizar_trueques(request):
    usuario_actual = get_user_model().objects.get(pk=request.user.id)
   
    # Obtener la filial asociada al usuario actual
    filial_usuario = usuario_actual.filial_nombre
    
    # Obtener la fecha actual
    today = "08/06/2024"

    # Inicializar trueques con una lista vacía
    trueques = []

    # Filtrar los turnos basados en la fecha y la filial del usuario
    turnos = Turno.objects.filter( filial__nombre=filial_usuario)

    # Verificar si se encontraron turnos para la fecha y la filial del usuario
    if turnos.exists():
        # Si se encontraron turnos, obtener el primero
        turno_actual = turnos.first()
        
        # Filtrar los Trueques basados en el turno actual y otros criterios
        query = request.GET.get('q')
        if query:
            trueques = Trueque.objects.filter(
                Q(codigo_confirmacion_solicitante=query) | Q(codigo_confirmacion_receptor=query),
                turno=turno_actual  # Filtrar por el turno actual
            )
            if not trueques.exists():
                messages.error(request, 'No se encontró ningún trueque con el código proporcionado.')
        else:
            trueques = Trueque.objects.filter(turno=turno_actual, aceptado=False, confirmado=True)
    else:
        # Si no se encontraron turnos para la fecha y la filial del usuario, manejar la situación apropiadamente
        messages.error(request, 'No se encontraron turnos para la fecha y la filial especificadas.')
        

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
    trueque.fecha_efectivizacion = timezone.now().date() # Asigna la fecha y hora actual
    solicitud = Solicitud.objects.filter(solicitante=trueque.solicitante, publicacion__usuario=trueque.receptor).first()

    if solicitud:
        solicitud.realizado = True
        print("entro")
        solicitud.publicacion.estado=False
        solicitud.save()

    trueque.save()
    enviar_correo_ayudante(trueque.solicitante)
    enviar_correo_ayudante(trueque.receptor)


    return redirect('efectivizar_trueque')


def rechazar_efectivizacion(request, id):
    print(id)
    try:
        trueque = Trueque.objects.get(id=id)
    except Trueque.DoesNotExist:
        # Manejar el caso en que no se encuentre el Trueque con el ID proporcionado
        messages.error(request, 'El Trueque no existe.')
        return redirect('efectivizar_trueque')
    
    solicitud = Solicitud.objects.filter(solicitante=trueque.solicitante, publicacionOfrecida__usuario=trueque.receptor).first()

    if solicitud:
        # Reactivar las publicaciones
        solicitud.estado = False
        solicitud.publicacion.trueque = False
        solicitud.publicacionOfrecida.trueque = False

        solicitud.publicacionOfrecida.estado = False
        solicitud.publicacion.save()
        solicitud.publicacionOfrecida.save()
         
        # Eliminar la solicitud
        solicitud.delete()

    # Eliminar el Trueque
    trueque.delete()

    messages.success(request, 'El trueque ha sido rechazado y las publicaciones reactivadas.')
    return redirect('efectivizar_trueque')

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
            solicitud.estado=False
            solicitud.publicacion.trueque = False
            solicitud.publicacionOfrecida.trueque = False

            solicitud.publicacionOfrecida.estado = False
            solicitud.publicacion.save()
            solicitud.publicacionOfrecida.save()
            # Eliminar la solicitud
            solicitud.delete()

        # Eliminar el trueque
        trueque.delete()

        # Mensaje de éxito
        messages.success(request, 'El usuario ha sido penalizado y las publicaciones reactivadas.')

    # Redireccionar a la página de efectivizar_trueques independientemente del método de solicitud
    return redirect('efectivizar_trueque')
