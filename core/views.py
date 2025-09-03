from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from core.serializers import ActivationCodeSerializer, LoginSerializer
from creator.models import Creator
from creator.serializers import CreatorSerializer 

class RegisterView(generics.CreateAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        activation_code = user.activation_code

        send_mail(
            'Activación de cuenta',
            f'Por favor activa tu cuenta con el sgte codigo: {activation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = authenticate(
                username=email, password=serializer.validated_data['password'])

            if user is not None:
                if not user.is_active:
                    return Response({'error': 'Cuenta no activa.'}, status=status.HTTP_403_FORBIDDEN)

                refresh = RefreshToken.for_user(user)
                creator_data = CreatorSerializer(user).data

                return Response({
                    'user': creator_data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            return Response({'error': 'Credenciales incorrectas.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    def post(self, request):
        serializer = ActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            activation_code = serializer.validated_data['activation_code']
            try:
                user = Creator.objects.get(activation_code=activation_code)

                if user.is_active:
                    return Response({"message": "La cuenta ya está activada."}, status=status.HTTP_400_BAD_REQUEST)

                # Activa la cuenta
                user.is_active = True
                user.save()

                return Response({"message": "Cuenta activada exitosamente!"}, status=status.HTTP_200_OK)

            except Creator.DoesNotExist:
                return Response({"error": "Código de activación inválido."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

