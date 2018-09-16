from rest_framework import generics
from RestAPI.permissions import IsPetPermission

class PermissionMixin():
    permission_classes = (IsPetPermission,)