from rest_framework import views, mixins, generics, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from . import serializers, models, common
from django.db.models import Count
from RestAPI.permissions import IsPetPermission
from django.contrib.auth import logout

class TestView(common.PermissionMixin, views.APIView):
    permission_classes = (IsPetPermission,)
    def get(self, request):
        print(request.entity.comments)

        return Response(data = "Hello!", status=200)

class AuthTestView(views.APIView):
    permission_classes = (IsPetPermission,)

    def get(self, request):
        for key in request.META:
            print(key)
            if key == 'HTTP_CNAME':
                print(request.META[key])

        return Response(status=200)

    def post(self, request):
        print(request.data)
        return Response(data = {"username":request.user.username}, status=200)

class CookieChecker(views.APIView):
    def get(self, request):
        print(request.COOKIES)
        return Response(status=200)

class LogOut(views.APIView):
    def get(self, request):
        logout(request)
        return Response(status=200)