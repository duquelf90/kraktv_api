from rest_framework import serializers
from .models import Creator, SocialLink
from django.contrib.auth import authenticate

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ["id", "platform", "url", "order"]


class SocialLinkListSerializer(serializers.Serializer):
    links = SocialLinkSerializer(many=True)
    
    
class CreatorSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, required=False, allow_empty=True)
    class Meta:
        model = Creator
        fields = [
            "username",
            "email",
            "password",
            "full_name",
            "phone",
            "country",
            "profile_image",
            "social_links",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data.pop('social_links', None)
        user = Creator(
            username=validated_data["username"],
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            phone=validated_data["phone"],
            country=validated_data["country"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user




