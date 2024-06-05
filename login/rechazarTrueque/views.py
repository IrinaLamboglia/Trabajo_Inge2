# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Solicitud
from django.core.mail import send_mail

from django.conf import settings

def rechazar_trueque(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    if request.method == 'POST':
        solicitud.rechazar()
        enviar_email_rechazo_turno(solicitud)
        solicitud.delete()
        messages.success(request, 'El trueque ha sido rechazado con éxito.')
        return redirect('misTrueques')
    
    return render(request, 'rechazarTrueque/rechazar_trueque.html', {'solicitud': solicitud})

def enviar_email_rechazo_turno(solicitud):
    mensaje = f"""
    Hola {solicitud.solicitante.username},

    Lamentamos informarte que tu solicitud de trueque para el producto '{solicitud.publicacion.titulo}' ha sido rechazada por el receptor.

    Gracias,
    El equipo de Cáritas
    """
    send_mail(
        'Solicitud de Trueque Rechazada',
        mensaje,
        settings.EMAIL_HOST_USER,
        [solicitud.solicitante.email],
        fail_silently=False,
    )
