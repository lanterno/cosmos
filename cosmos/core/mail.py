from templated_mail.mail import BaseEmailMessage


class DynamicHostMixin:

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request:
            domain = self.request.META.get('HTTP_ORIGIN')
            domain = domain and domain.replace("https://", "").replace("http://", "")
            context['domain'] = domain or context.get('domain')
        return context


class DynamicHostBaseEmailMessage(DynamicHostMixin, BaseEmailMessage):
    pass

