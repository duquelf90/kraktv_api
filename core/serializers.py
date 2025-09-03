
from rest_framework import serializers
from django.contrib.auth import authenticate

class ActivationCodeSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Credenciales incorrectas.")
        return data