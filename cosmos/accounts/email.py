from djoser.email import ActivationEmail as OldActivationEmail
from cosmos.core.mail import DynamicHostMixin


class ActivationEmail(DynamicHostMixin, OldActivationEmail):
    pass
