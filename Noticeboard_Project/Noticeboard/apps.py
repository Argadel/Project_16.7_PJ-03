from django.apps import AppConfig


class NoticeboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Noticeboard'

    def ready(self):
        from . import signals
