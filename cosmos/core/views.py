from django.views.generic import TemplateView
from rest_framework_swagger import renderers

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .docs import SCHEMA


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        return Response(SCHEMA)


class SocialCallBackView(TemplateView):
    template_name = 'callback.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update({'data': self.request.GET.dict()})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update({'data': self.request.POST.dict()})
        return self.render_to_response(context)

