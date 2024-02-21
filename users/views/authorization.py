from django.contrib.auth import authenticate, login, logout
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from users.models import MyUser
from users.serializers import RegistrationSerializer, VerificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.utils import send_confirmation_email


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            send_confirmation_email(serializer.data['email'])
            return Response(
                {
                    'message': 'მომხმარებელი წარმატებით დარეგისტრირდა',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        global email
        try:
            if not (request.data['email'] and request.data['password']):
                return Response(
                    {'error': 'საჭირო ველები შესავსებია'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            email = request.data['email']
            password = request.data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                auth_data = get_tokens_for_user(request.user)
                return Response(
                    {'message': 'თქვენ წარმატებით გაიარეთ ავტორიზაცია', **auth_data, "user_id": user.id},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'მონაცემები არასწორია'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except:
            return Response(
                {'error': 'შეცდომა დალოგინებისას'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {'message': 'თქვენ წარმატებით გამოხვედით სისტემიდან'},
            status=status.HTTP_200_OK
        )

class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerificationSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = MyUser.objects.filter(email=email)

                if not user.exists():
                    return Response({
                        'message': 'იმეილი არ არსებობს',
                    },
                        status=status.HTTP_404_NOT_FOUND)

                if user[0].is_email_confirmed:
                    return Response(
                        {'message': 'იმეილი უკვე ვერიფიცირებულია'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if user[0].otp != otp:
                    return Response({
                        'message': 'არასწორი კოდი',
                    },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                user = user.first()
                user.is_email_confirmed = True
                user.save()

                return Response(
                    {
                        'message': 'თქვენ წარმატებით გაიარეთ ვერიფიკაცია',
                        'data': serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {'error': 'შეცდომა ვერიფიკაციისას'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from rest_framework.permissions import IsAuthenticated


class CheckTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(
                {'is_valid': True},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'is_valid': False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
