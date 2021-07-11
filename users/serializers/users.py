""" Users Serializers """

#Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Models
from django.contrib.auth.models import User
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """ Profile model serializer """

    class Meta:
        model = Profile
        fields = ['age', 'city', 'country',
                  'header_img', 'profile_picture',
                  'followers', 'likes', 'posts']


class UserSerializer(serializers.ModelSerializer):
    """ User Serializer """

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'profile']