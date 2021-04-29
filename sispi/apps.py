from django.apps import AppConfig


class SispiConfig(AppConfig):
    name = 'sispi'

    def ready(self):
        import sispi.signals
