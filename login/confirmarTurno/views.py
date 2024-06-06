
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Trueque
from django.core.mail import send_mail
from django.conf import settings
import datetime

from django.urls import reverse
def confirmar_turno(request, trueque_id):
    trueque = get_object_or_404(Trueque, id=trueque_id)
    token = request.GET.get('token')
    
    if trueque.solicitante != request.user or trueque.token != token:
        messages.error(request, "Usuario inválido.")
        return redirect('inicio')
    
    if trueque.confirmado:
        messages.error(request, "Ese turno ya fue confirmado/rechazado.")
        return redirect('inicio')
    
    if request.method == "POST":
        confirmar = request.POST.get("confirmar")
        cancelar = request.POST.get("cancelar")
        
        if confirmar == "yes":
            trueque.confirmado = True
            trueque.save()
            enviar_email_confirmacion_final(trueque)  # Enviar correo de confirmación final a ambos
            messages.success(request, "El turno ha sido confirmado exitosamente.")
            return redirect('inicio')
        
        
        else:
            messages.error(request, "Debe confirmar o cancelar el turno para continuar.")

    context = {
        'trueque': trueque,
        'turno': trueque.turno,
        'filial': trueque.filial,
    }
    return render(request, 'confirmarTurno/confirmar_turno.html', context)


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
