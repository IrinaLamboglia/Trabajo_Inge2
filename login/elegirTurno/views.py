from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from core.models import Trueque, Turno, Filial
from django.conf import settings
from django.urls import reverse
from django.contrib import messages

@login_required
def elegir_turno(request, trueque_id):
    trueque = get_object_or_404(Trueque, id=trueque_id)
    token = request.GET.get('token')

    # Validación del token y del usuario
    if trueque.receptor != request.user or trueque.token != token:
        messages.error(request, "Token invalido.")
        return redirect('inicio')
    
    # Verificar si ya se ha elegido un turno
    if trueque.turno:
        messages.error(request, "Ya se selecciono un turno.")
        return redirect('inicio')

    if request.method == "POST":
        turno_id = request.POST.get("turno")
        if turno_id:
            try:
                turno = Turno.objects.get(id=turno_id)
                if turno.cupos_disponibles > 0:
                    if trueque.turno != turno:
                        turno.cupos_disponibles -= 1
                        turno.save()

                    trueque.turno = turno
                    trueque.filial = turno.filial
                    trueque.save()

                    trueque.generar_codigos_confirmacion()
                    enviar_email_confirmacion(trueque,request)

                    return redirect('misTrueques')
                else:
                    error_message = "El turno seleccionado ya no tiene cupos disponibles."
            except Turno.DoesNotExist:
                error_message = "El turno seleccionado no existe."
        else:
            error_message = "Por favor, selecciona un turno."
    else:
        error_message = None

    filial_id = request.GET.get('filial')
    if filial_id:
        turnos_disponibles = Turno.objects.filter(cupos_disponibles__gt=0, fecha__gte=timezone.now(), filial_id=filial_id)
    else:
        turnos_disponibles = Turno.objects.filter(cupos_disponibles__gt=0, fecha__gte=timezone.now())

    filiales = Filial.objects.all()

    context = {
        'trueque': trueque,
        'turnos_disponibles': turnos_disponibles,
        'filiales': filiales,
        'selected_filial': filial_id,
        'error_message': error_message
    }
    return render(request, 'elegirTurno/elegir_turno.html', context)

def enviar_email_confirmacion(trueque, request):
    link = reverse('confirmar_turno', args=[trueque.id])
    print(request)
    url = request.build_absolute_uri(f"{link}?token={trueque.token}")

    mensaje_solicitante = f"""
    Hola {trueque.solicitante.username},

    El receptor ha elegido un turno para el trueque. Por favor, confirma el
    {url}

    Gracias,
    El equipo de Cáritas
    """

    send_mail(
        'Confirmación de Turno de Trueque',
        mensaje_solicitante,
        settings.EMAIL_HOST_USER,
        [trueque.solicitante.email],
        fail_silently=False,
    )