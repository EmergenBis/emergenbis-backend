''' User edit permission'''

from rest_framework.permissions import BasePermission
#from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from users.models import Profile

class IsOwnProfile(BasePermission):

    def has_object_permission(self, request, view, obj):

        token = request.headers['Authorization']
        token = token.split(' ')
        token = token.objects.get(key=token[1])
        print(token.user)

        try:
            User.objects.get(username=request.user.username)
            #Token.objects.get()
        except User.DoesNotExist:
            return False
        
        return True