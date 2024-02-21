from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import MyUser
from users.serializers import ChangePasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
