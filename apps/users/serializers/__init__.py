from django.contrib.auth import get_user_model

from rest_framework import serializers

from .validations import ValidationUser

User = get_user_model()


class MetaUser:
    model = User

    fields = [
        "id",
        "first_name",
        "last_name",
        "curp",
        "number_phone",
        "address",
        "email",
        "turn",
        "photo",
        "groups",
    ]

class UserListSerializer(serializers.ModelSerializer):
    turn = serializers.CharField(source="get_turn_display", default=None, read_only=True)
     
    class Meta(MetaUser):
        model = User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta(MetaUser):
        model = User


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta(MetaUser):
        model = User
        
        
