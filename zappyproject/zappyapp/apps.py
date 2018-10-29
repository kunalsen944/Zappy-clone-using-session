from django.apps import AppConfig


class ZappyappConfig(AppConfig):
    name = 'zappyapp'

    def ready(self):
        import zappyapp.signals
