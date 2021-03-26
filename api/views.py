import hashlib
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .models import YamdbUser
from .serializers import ConfirmationCodeSerializer, YamdbUserSerializer


class YamdbUserViewSet(viewsets.ModelViewSet):
    queryset = YamdbUser.objects.all()
    serializer_class = YamdbUserSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['email']


class YamdbUserMeViewSet(YamdbUserViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        id = self.request.user.pk
        return YamdbUser.objects.filter(id=id)

    def update(self, request):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class YamdbUsernameViewSet(YamdbUserViewSet):
    pagination_class = None

    def get_queryset(self):
        username = self.kwargs['username']
        return YamdbUser.objects.filter(username=username)

    def update(self, request, username):
        user = get_object_or_404(YamdbUser, username=username)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, username):
        user = get_object_or_404(YamdbUser, username=username)
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Registration(APIView):
    permission_classes = [AllowAny]
    
    def ConfirmationCodeGenerate(self, email):
        confirmation_code = hashlib.md5('{}{}'.format(
                            email, settings.SECRET_KEY).encode(
                            'utf-8')).hexdigest()
        return confirmation_code


class GetConfirmationCode(Registration):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            serializer.save(is_active = False, username=email)
            confirmation_code = self.ConfirmationCodeGenerate(email)
            return Response(f'Код подтверждения {confirmation_code} для {email}', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetToken(Registration):
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    def post(self, request):
        email = request.data['email']
        confirmation_code = request.data['confirmation_code']
        confirmation_code_check = self.ConfirmationCodeGenerate(email)
        if confirmation_code == confirmation_code_check:
            user = get_object_or_404(YamdbUser, email=email)
            token = self.get_tokens_for_user(user)
            user.is_active=True
            user.save()
            return Response(token, status=status.HTTP_200_OK)
        return Response(
            'Ошибка в коде или email. Получите новый код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )