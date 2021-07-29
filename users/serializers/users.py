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

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.username)
        instance.last_name = validated_data.get('last_name', instance.username)
        instance.email = validated_data.get('email', instance.username)
        instance.save()

        profile.age =  profile_data.get('age', profile.age)
        profile.city =  profile_data.get('city', profile.city)
        profile.country =  profile_data.get('country', profile.country)
        profile.header_img =  profile_data.get('header_img', profile.header_img)
        profile.profile_picture =  profile_data.get('profile_picture', profile.profile_picture)
        profile.save()

        return instance
        

class NewUserSerializer(serializers.ModelSerializer):
    ''' Return the data for a new user '''
    
    class Meta:
        model = User
        fields = ['username']




