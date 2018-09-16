from rest_framework import generics
from .. import models, serializers
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

class AuthorizationView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AuthorizationSerializer

    def get_queryset(self):
        queryset = self.request.user.entity.authorizations.all()
        return queryset

class AuthorizationActiveView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AuthorizationSerializer

    def get_queryset(self):
        time = datetime.now()
        queryset = self.request.user.entity.authorizations.filter(start_date__lt = time).filter(expiry_date__gt = time)
        return queryset

''' class AuthorizationLView(generics.ListAPIView):
    serializer_class = serializers.AuthorizationLSerializer
    queryset = models.Authorization.objects.all()

class AuthorizationRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AuthorizationRUDSerializer
    queryset = models.Authorization.objects.all()

class AuthorizationEScopeLCView(generics.ListCreateAPIView):
    serializer_class = serializers.AuthorizationLCSerializer
    
    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(models.Entity.objects.all(), **filter_kwargs)
        queryset = obj.authorizations
        return queryset

    def create(self, request, *args, **kwargs):
        data=request.data
        data['entity'] = kwargs['pk']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

 '''