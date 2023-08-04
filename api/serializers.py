import datetime

from rest_framework import serializers
from user.models import UserAccount
from post.models import Announcement
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    image_link = serializers.SerializerMethodField("get_image_link")

    class Meta:
        model = UserAccount
        fields = ("password", "email", "image_link", "first_name", "last_name", "image")

        extra_kwargs = {
            'password': {'write_only': True},
            'image': {'write_only': True},
        }

    def create(self, validate_data):
        validate_data["password"] = make_password(validate_data["password"])
        return super(UserSerializer, self).create(validate_data)

    def get_image_link(self, obj):
        try:
            up = UserProfile.objects.get(user=obj)
            return up.image.url
        except Exception:
            return None

class AnnouncementSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True, source="owner.email")
    class Meta:
        model = Announcement
        fields = ("id", "title", "content", "owner", "accept", "views_count", "picture")

        extra_kwargs = {
            'id': {'read_only': True},
        }
