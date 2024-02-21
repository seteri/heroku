
from django.shortcuts import render
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm as BaseResetPasswordConfirm, \
    ResetPasswordValidateToken
from rest_framework import status
from rest_framework.response import Response
from users.utils import send_password_reset_instruction


class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            email = request.data.get('email')
            token_id = ResetPasswordToken.objects.filter(user__email=email).first().key
            print(token_id)
            send_password_reset_instruction(email, token_id)

            return Response({'success': 'პაროლის შეცვლის ინსტრუქცია გამოგზავნილია თქვენს იმეილზე'},
                            status=status.HTTP_200_OK)


class SetNewPassword(BaseResetPasswordConfirm):
    def get(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print(response)


        return Response('dedistraki')


