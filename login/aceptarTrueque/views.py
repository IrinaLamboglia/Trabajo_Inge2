from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from core.models import Solicitud, Trueque
from django.urls import reverse
from django.conf import settings
import secrets

@login_required
def aceptar_trueque(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if request.method == 'POST':
        solicitud.aceptar()
        trueque = Trueque.objects.create(
            solicitante=solicitud.solicitante,
            receptor=request.user,
        )
        trueque.generar_codigos_confirmacion()
        trueque.save()

        # Cancelar otras solicitudes para el mismo producto eliminándolas de la base de datos
        solicitudesReseptor = Solicitud.objects.filter(publicacion=solicitud.publicacion).exclude(id=solicitud_id)
        for solicitud in solicitudesReseptor:
            enviar_email_cancelacion(solicitud)
            solicitud.delete()

        solicitudesReseptor = Solicitud.objects.filter(publicacion=solicitud.publicacionOfrecida).exclude(id=solicitud_id)
        for solicitud in solicitudesReseptor:
            enviar_email_cancelacion(solicitud)
            solicitud.delete()    

        enviar_email_elegir_turno(trueque, request,solicitud)
        
        return redirect('misTrueques')
    
    return render(request, 'aceptarTrueque/aceptar_trueque.html', {'solicitud': solicitud})


def enviar_email_cancelacion(solicitud):
    mensaje = f"""
    Hola {solicitud.solicitante.username},

    Lamentamos informarte que tu solicitud de trueque para el producto '{solicitud.publicacion.titulo}' ha sido cancelada porque el producto ya no está disponible.

    Gracias,
    El equipo de Cáritas
    """
    send_mail(
        'Solicitud de Trueque Cancelada',
        mensaje,
        settings.EMAIL_HOST_USER,
        [solicitud.solicitante.email],
        fail_silently=False,
    )

def enviar_email_elegir_turno(trueque, request,solicitud):
    # Construir el enlace para elegir el turno
    link = reverse('elegir_turno', args=[trueque.id])
    url = request.build_absolute_uri(f"{link}?token={trueque.token}")
    
    # Mensaje para el solicitante
    mensaje_solicitante = f"""
    Hola {trueque.solicitante.username},

    Tu solicitud de trueque para el producto '{solicitud.publicacion.titulo}' ha sido aceptada. El receptor puede elegir un turno disponible y contactarte.

    Contacta con {trueque.receptor.username} para poder ponerse de acuerdo con el turno a elegir.
    
    Gracias,
    El equipo de Cáritas
    """
    
    # Mensaje para el receptor
    mensaje_receptor = f"""
    Hola {trueque.receptor.username},

    Has aceptado una solicitud de trueque para el producto '{solicitud.publicacion.titulo}'. Por favor, elige un turno disponible haciendo clic en el siguiente enlace:

    {url}
    
    Contacta con {trueque.solicitante.username} para coordinar un turno para efectivizar el trueque.

    Gracias,
    El equipo de Cáritas
    """

    # Enviar correo al solicitante
    send_mail(
        'Contacta con tu compañero de trueque',
        mensaje_solicitante,
        settings.EMAIL_HOST_USER,
        [trueque.solicitante.email],
        fail_silently=False,
    )
    
    # Enviar correo al receptor con el enlace para elegir el turno
    send_mail(
        'Elige un turno para tu trueque',
        mensaje_receptor,
        settings.EMAIL_HOST_USER,
        [trueque.receptor.email],
        fail_silently=False,
    )
