from django.apps import AppConfig


class TrackrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trackr'

    def ready(self):
        import trackr.signals
