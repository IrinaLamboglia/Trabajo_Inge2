from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import datetime
from core.models import Trueque
def rechazar_turno(request, trueque_id):
    trueque = get_object_or_404(Trueque, id=trueque_id)
    token = request.GET.get('token')
    
    if trueque.solicitante != request.user or trueque.token != token:
        messages.error(request, "Usuario inválido.")
        return redirect('inicio')
    
    if trueque.confirmado:
        messages.error(request, "Ese turno ya fue confirmado/rechazado.")
        return redirect('inicio')
    
    if trueque.turno.fecha - datetime.date.today() < datetime.timedelta(days=1):
        messages.error(request, 'La cancelación requiere al menos 24 horas de antelación.')
    else:
        trueque.confirmado = False
        trueque.save()
        enviar_email_elegir_turno(trueque, request)
        messages.success(request, 'El turno ha sido cancelado exitosamente.')
        
    return redirect('inicio')

def enviar_email_elegir_turno(trueque, request):
    # Generar un nuevo token para el trueque
    trueque.generar_token()

    # Construir el enlace para elegir el turno
    link = reverse('elegir_turno', args=[trueque.id])
    url = request.build_absolute_uri(f"{link}?token={trueque.token}")
    
    mensaje_receptor = f"""
    Hola {trueque.receptor.username},

    Has aceptado una solicitud de trueque y el solicitante ha rechazado el turno del trueque. Por favor, elige un turno disponible haciendo clic en el siguiente enlace, nuevamente:
    {url}
    
    Contacta con {trueque.solicitante.username} para coordinar un turno para efectivizar el trueque.

    Gracias,
    El equipo de Cáritas
    """

    send_mail(
        'Elige otro turno para tu trueque',
        mensaje_receptor,
        settings.EMAIL_HOST_USER,
        [trueque.receptor.email],
        fail_silently=False,
    )
