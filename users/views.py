from .models import *
from reviews.utils import ObjectMixin
from rest_framework.response import Response

from .permissions import IsAdminorMe

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserEmailSerializer, ConfirmationCodeSerializer, UserSerializer


@api_view(['POST'])
def get_confirmation_code(request):
    username = request.data.get('username')
    serializer = UserEmailSerializer(data=request.data)
    email = request.data.get('email')

    if serializer.is_valid():
        if username is not None:
            user = User.objects.filter(
                username=username) | User.objects.filter(email=email)
            if len(user) == 0:
                User.objects.create_user(username=username, email=email)
            else:
                return Response(serializer.errors, status=status.HTTP_418_IM_A_TEAPOT)
        user = get_object_or_404(User, email=email)
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Код подтверждения'
        message = f'Ваш код подтверждения: {confirmation_code}'
        send_mail(mail_subject, message, 'Yamdb.ru <admin@yamdb.ru>',
                  [email], fail_silently=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)

        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ObjectMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminorMe]
    model = User
    serializer = UserSerializer


def AnyUser(request, username):
    user = get_object_or_404(User, username=username)
    return user
