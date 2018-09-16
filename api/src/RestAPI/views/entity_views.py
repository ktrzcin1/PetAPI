from .. import models, serializers, permissions
from rest_framework import generics
from . import common

class EntityView(common.PermissionMixin, generics.RetrieveAPIView):
    serializer_class = serializers.EntitySerializer

    def get_object(self):
        obj = self.request.entity
        return obj

class EntityLCView(generics.ListCreateAPIView, common.PermissionMixin):
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntityBasicSerializer

class EntityRUDView(generics.RetrieveUpdateDestroyAPIView, common.PermissionMixin):
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntityBasicSerializer

class EntityPETView(generics.RetrieveAPIView, common.PermissionMixin):
    serializer_class = serializers.EntityBasicSerializer

    def get_object(self):
        name = self.request.META.get('HTTP_PETNAME', None)
        entity = models.Entity.objects.getEntity(name)
        return entity
