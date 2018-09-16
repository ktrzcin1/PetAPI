from django.contrib.auth.middleware import PersistentRemoteUserMiddleware
from RestAPI.models import Entity

class AuthMiddleware:

    HEADER_NAME = 'HTTP_CNAME'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            header = request.META[self.HEADER_NAME] # in reality it is entities common_name
            raw_name = list(filter(lambda s: s.startswith('CN='), header.split(',')))[0]
            print(raw_name)
            common_name = raw_name[len('CN='):]
            print(common_name)
            entity = Entity.objects.get(common_name=common_name)
            request.entity = entity
        except Exception:
            request.entity = None

        response = self.get_response(request)

        return response