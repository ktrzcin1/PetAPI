from rest_framework import serializers
from .. import models

class EntityBasicSerializer(serializers.ModelSerializer):
    '''
    EntityCreateSerialzier():
        id = IntegerField(label='ID', read_only=True)
        common_name = CharField(max_length=45)
        name = CharField(max_length=45)
        address = CharField(max_length=45)
        contact = CharField(max_length=45)
        comments = CharField(style={'base_template': 'textarea.html'})
    '''
    class Meta:
        model = models.Entity
        fields='__all__'
        read_only_fields = ('created')

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entity
        fields = '__all__'


