from rest_framework import serializers
from .. import models
from . import file_serializers


class JobIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = ('id',)
        read_only_fields = ('id',) 

class JobSerializer(serializers.ModelSerializer):
    input_data      = serializers.PrimaryKeyRelatedField(many=True, required = False, queryset = models.File.objects.all())
    output_data     = serializers.PrimaryKeyRelatedField(many = True, required = False, queryset = models.File.objects.all())

    job_previous    = JobIDSerializer(many = True, read_only = True)
    job_next        = JobIDSerializer(many = True, read_only = True)
   
    out_file        = file_serializers.FileSerializer(read_only = True)
    err_file        = file_serializers.FileSerializer(read_only = True)

    class Meta:
        model = models.Job
        fields = ('__all__')
        read_only_fields = ('job_status', 'started_date', 'completed_date')
        extra_kwargs = {
            'task' : {'write_only': True}
        }

class JobLogSerializer(serializers.ModelSerializer):
    out_file        = file_serializers.FileSerializer(read_only = True)
    err_file        = file_serializers.FileSerializer(read_only = True)

    class Meta:
        model = models.Job
        fields = ('id', 'saved_id', 'job_status', 'exit_code', 'out_file', 'err_file')
        read_only_fields=('id', 'saved_id', 'job_status', 'exit_code')

class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = ('id', 'saved_id', 'job_status', 'exit_code')
        read_only_fields=('id', 'saved_id', 'job_status', 'exit_code')
        
        
        