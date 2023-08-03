import datetime

from rest_framework import serializers
from user.models import UserAccount


class UserSerializer(serializers.ModelSerializer):
    image_link = serializers.SerializerMethodField("get_image_link")

    class Meta:
        model = User
        fields = ("password", "email", "image_link", "first_name", "last_name", "image")

        extra_kwargs = {
            'password': {'write_only': True},
            'image': {'write_only': True},
        }

    def get_image_link(self, obj):
        try:
            up = UserProfile.objects.get(user=obj)
            return up.image.url
        except Exception:
            return None
