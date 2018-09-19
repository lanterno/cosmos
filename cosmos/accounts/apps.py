from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'cosmos.accounts'
    verbose_name = 'Accounts'

    def ready(self):
        from . import signals  # register signals
