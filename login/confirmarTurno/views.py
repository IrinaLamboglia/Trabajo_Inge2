
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Trueque
from django.core.mail import send_mail
from django.conf import settings
import datetime

from django.urls import reverse
  
def confirmar_turno(request, trueque_id):
    trueque = get_object_or_404(Trueque, id=trueque_id)
    print(request.GET)
    token = request.GET.get('token')
    
    if trueque.solicitante != request.user or trueque.token != token:
        messages.error(request, "user inválido.")
        return redirect('inicio')
    
    if trueque.confirmado:
        messages.error(request, "Ese turno ya fue confirmado/rechazado.")
        return redirect('inicio')
    
    if request.method == "POST":
        print ("entra post")
        confirmar = request.POST.get("confirmar")
        cancelar = request.POST.get("cancelar")
        
        if confirmar == "yes":
            trueque.confirmado = True
            trueque.save()
            enviar_email_confirmacion_final(trueque)  # Enviar correo de confirmación final a ambos
            messages.success(request, "El turno ha sido confirmado exitosamente.")
            return redirect('inicio')
        
        elif cancelar == "yes":
            if trueque.turno.fecha - datetime.date.today() < datetime.timedelta(days=1):
                messages.error(request, 'La cancelación requiere al menos 24 horas de antelación.')
            else:
                enviar_email_elegir_turno(trueque,request)
                messages.success(request, 'El turno ha sido cancelado exitosamente.')
            return redirect('inicio')
        else:
            messages.error(request, "Debe confirmar o cancelar el turno para continuar.")

    context = {
        'trueque': trueque,
        'turno': trueque.turno,
        'filial': trueque.filial,
    }
    return render(request, 'confirmarTurno/confirmar_turno.html', context)



def enviar_email_elegir_turno(trueque,request):
    # Construir el enlace para elegir el turno
    link = reverse('elegir_turno', args=[trueque.id])
    url = request.build_absolute_uri(f"{link}?token={trueque.token}")
    
    # Mensaje para el receptor
    mensaje_receptor = f"""
    Hola {trueque.receptor.username},

    Has aceptado una solicitud de trueque y el solicitante rechazo el turno del trueque. Por favor, elige un turno disponible haciendo clic en el siguiente enlace, nuevamente:
    {url}
    
    Contacta con {trueque.solicitante.username} para coordinar un turno para efectivizar el trueque.

    Gracias,
    El equipo de Cáritas
    """

    
    # Enviar correo al receptor con el enlace para elegir el turno
    send_mail(
        'Elige un turno para tu trueque',
        mensaje_receptor,
        settings.EMAIL_HOST_USER,
        [trueque.receptor.email],
        fail_silently=False,
    )

def enviar_email_confirmacion_final(trueque):
    mensaje_solicitante = f"""
    Hola {trueque.solicitante.username},

    Has confirmado el turno para tu trueque. Aquí están los detalles:
    
    Fecha del Turno: {trueque.turno.fecha}
    Filial: {trueque.filial.nombre}
    Tu código de confirmación: {trueque.codigo_confirmacion_solicitante}

    ¡Nos vemos pronto!
    """
    
    mensaje_receptor = f"""
    Hola {trueque.receptor.username},

    El solicitante ha confirmado el turno para tu trueque. Aquí están los detalles:
    
    Fecha del Turno: {trueque.turno.fecha}
    Filial: {trueque.filial.nombre}
    Tu código de confirmación: {trueque.codigo_confirmacion_receptor}

    ¡Nos vemos pronto!
    """
    
    send_mail(
        'Confirmación Final de Turno de Trueque',
        mensaje_solicitante,
        settings.EMAIL_HOST_USER,
        [trueque.solicitante.email],
        fail_silently=False,
    )
    
    send_mail(
        'Confirmación Final de Turno de Trueque',
        mensaje_receptor,
        settings.EMAIL_HOST_USER,
        [trueque.receptor.email],
        fail_silently=False,
    )
