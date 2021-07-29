#Django REST framework
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwnProfile

#Models
from django.contrib.auth.models import User
from users.models import Profile

#Serializer
from users.serializers.users import UserSerializer, NewUserSerializer
from users.serializers.signup import UsersSignupSerializer
from users.serializers.verified import AccountVerificationSerializer



class UserListView (ListAPIView):
    """ List all the users with pagination """

    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination 

class ProfileCompletionViewSet(mixins.UpdateModelMixin,
                               viewsets.GenericViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnProfile]

    


@api_view(['POST'])
def signup(request):

    if request.method == 'POST':
        serializer = UsersSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user =serializer.save()
        data = NewUserSerializer(user).data
        return Response(data)


@api_view(['POST'])
def account_verification(request):
    """ Account verification API View """
    if request.method == 'POST':
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Account verification success'}
        return Response(data, status=status.HTTP_200_OK)
