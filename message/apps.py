from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MessageConfig(AppConfig):
    name = 'message'
    verbose_name = _('message')

    def ready(self):
        import message.signals  # noqa
