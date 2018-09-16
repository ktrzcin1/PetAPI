from rest_framework import serializers
from .. import models


class FileSerializer(serializers.ModelSerializer):
    '''Serializes to: id, name, comments, path'''
    class Meta:
        model = models.File
        fields=('__all__')
        
        extra_kwargs = {
            'task' : {'write_only': True}
        }

class FileIDSerializer(serializers.ModelSerializer):
    '''Read only, ID serializer'''
    class Meta:
        model = models.File
        fields = ('id',)
        read_only_fields = ('id',)

