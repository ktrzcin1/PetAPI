from rest_framework import serializers
from .. import models

class AuthorizationSerializer(serializers.ModelSerializer):
    '''
    AuthorizationListSerializer():
        id = IntegerField(label='ID', read_only=True)
        subject = CharField(max_length=45)
        issue_date = DateTimeField()
        expiry_date = DateTimeField()
        fingerprint = CharField(max_length=45)
        entity = PrimaryKeyRelatedField(queryset=Entity.objects.all())
    '''
    class Meta:
        model = models.Authorization
        fields='__all__'
        read_only_fields = ('issue_date', 'expiry_date', 'fingerprint','id','subject')

        extra_kwargs = {
            'entity': {'write_only': True},
        }

class AuthorizationLSerializer(serializers.ModelSerializer):
    '''
    AuthorizationListSerializer():
        id = IntegerField(label='ID', read_only=True)
        subject = CharField(max_length=45)
        issue_date = DateTimeField()
        expiry_date = DateTimeField()
        fingerprint = CharField(max_length=45)
        entity = PrimaryKeyRelatedField(queryset=Entity.objects.all())
    '''
    class Meta:
        model = models.Authorization
        fields='__all__'

class AuthorizationRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Authorization
        fields='__all__'
        read_only=('entity', )