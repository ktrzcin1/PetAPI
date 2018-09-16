from rest_framework import serializers
from .. import models
from . import job_serializers, file_serializers


class TaskSerializer(serializers.ModelSerializer):
    ''' Required fields: entity
        Optional fields: parameters, comments, task_type, priority
        Serializes to: id, task_status, issued_date, started_date, completed_date, priority, parameters, comments, task_type'''

    jobs = job_serializers.JobSerializer(many = True, read_only = True)
    files = file_serializers.FileSerializer(many = True, read_only = True)
    log_file = file_serializers.FileSerializer(read_only = True)

    class Meta:
        model = models.Task
        fields=('__all__')
        read_only_fields = ('issued_date', 'started_date', 'completed_date', 'task_status', 'jobs', 'files', 'log_file')
        extra_kwargs = {
            'entity' : {'write_only': True}
        }


class TaskStatusSerializer(serializers.ModelSerializer):
    jobs = job_serializers.JobStatusSerializer(many=True, read_only = True)

    class Meta:
        model = models.Task
        fields = ('id', 'task_status', 'jobs')
        read_only_fields = ('id', 'task_status')


class TaskLogSerializer(serializers.ModelSerializer):
    jobs        = job_serializers.JobLogSerializer(many=True, read_only = True)
    log_file    = file_serializers.FileSerializer(read_only = True)

    class Meta:
        model = models.Task
        fields = ('id', 'task_status', 'jobs', 'log_file')
        read_only_fields = ('id', 'task_status')