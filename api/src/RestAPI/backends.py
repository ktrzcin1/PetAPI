from django.contrib.auth.backends import RemoteUserBackend

class DoNotCreateNewUserRemoteUserBackend(RemoteUserBackend):
    create_unknown_user = False