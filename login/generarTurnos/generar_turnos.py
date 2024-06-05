import datetime
from core.models import Turno, Filial

def generar_turnos():
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=60)

    current_date = today
    while current_date <= end_date:
        if current_date.weekday() in [5, 6]:  # 5 is Saturday, 6 is Sunday
            for filial in Filial.objects.all():
                if not Turno.objects.filter(fecha=current_date, filial=filial).exists():
                    Turno.objects.create(fecha=current_date, filial=filial, cupo_maximo=50, cupos_disponibles=50)
        current_date += datetime.timedelta(days=1)
