from django.shortcuts import render
from django.utils import timezone
from core.models import Trueque, Filial
from django.contrib.auth.decorators import login_required


def visualizar_trueques_diarios(request):
    
    # Intenta obtener la filial del ayudante actual
    try:
        filial = Filial.objects.get(ayudante=request.user)
    except Filial.DoesNotExist:
        filial = None
    
    # Obtén la fecha actual
    today = timezone.localtime().date()

    if filial:
        # Filtra los trueques efectivizados hoy y aceptados para la filial del ayudante
        trueques = Trueque.objects.filter(filial=filial, fecha_efectivizacion__date=today, aceptado=True)
    else:
        trueques = []

    context = {
        'trueques': trueques,
    }

    return render(request, 'visualizarTrueques/visualizar_trueques_diarios.html', context)
