from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from generarTurnos.generar_turnos import generar_turnos  # Ajusta el path si es necesario
        generar_turnos()
