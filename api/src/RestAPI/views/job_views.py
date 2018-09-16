from rest_framework import generics
from .. import models, serializers
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
import datetime

''' class JobTScopeLCView(generics.ListCreateAPIView):
    serializer_class = serializers.JobBasicSerializer

    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(models.Task.objects.all(), **filter_kwargs)
        queryset = obj.jobs
        return queryset

    def create(self, request, *args, **kwargs):
        data=request.data
        data['task'] = kwargs['pk']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class JobLView(generics.ListAPIView):
    serializer_class = serializers.JobBasicSerializer
    queryset = models.Job.objects.all()

class JobRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.JobBasicSerializer
    queryset = models.Job.objects.all()

class JobStartView(generics.CreateAPIView):
    def create(request, *args, **kwargs):
        filter_kwargs = {'id': kwargs['pk']}
        obj = get_object_or_404(models.Job.objects.all(), **filter_kwargs)
        obj.start_date = datetime.datetime.now()
        obj.save()
        return Response(status=status.HTTP_201_CREATED)

class JobFinishView(generics.CreateAPIView):
    def create(request, *args, **kwargs):
        filter_kwargs = {'id': kwargs['pk']}
        obj = get_object_or_404(models.Job.objects.all(), **filter_kwargs)
        obj.finish_date = datetime.datetime.now()
        obj.save()
        return Response(status=status.HTTP_201_CREATED) '''