from django.test import TestCase
from RestAPI import models

class EntityTest(TestCase):
    def test_create_entity(self):
        entity = models.Entity(common_name='EntityCommonName#1', name='EntityName#1',
                                address='EntityAddress#1', contact='EntityContact#1', comments='EntityComments#1')
        entity.save()
        
        db_entity = models.Entity.objects.all()[0]
        self.assertEqual(db_entity.common_name, 'EntityCommonName#1')
        self.assertEqual(db_entity.name, 'EntityName#1')
        self.assertEqual(db_entity.address, 'EntityAddress#1')
        self.assertEqual(db_entity.contact, 'EntityContact#1')
        self.assertEqual(db_entity.comments, 'EntityComments#1')