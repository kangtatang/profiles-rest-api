from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.
class HelloApiView(APIView):
    """ test api view """

    serializer_class = serializers.HelloSerializers

    def get(self, request, format=None):
        """ return a list of APIView features """
        an_apiview = [
            'Uses HTTP method as function (get, post, patch, put, delete)',
            'It is similar to a traditional django view',
            'Gives you the most control over your logic',
            'is mapped manully to URLS'
        ]

        return Response({'message':'Hello!','an_apiview':an_apiview})

    def post(self, request):
        """ create a hello message with our name """

        serializer = serializers.HelloSerializers(data = request.data)
        # cek apakah input valid atau tidak sesuai dengan rules di serializer
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        #jika tidak valid
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """ handles updating an object """

        return Response({'method':'put'})

    def patch(self, request, pk=None):
        """ patch request, only updates fields provided in request """

        return Response({'method':'patch'})

    def delete(self, request, pk=None):
        """ deletes an objects """

        return Response({'method':'delete'})


class HelloViewSet(viewsets.ViewSet):
    """ test api viewset """

    serializer_class = serializers.HelloSerializers

    def list(self, request):
        """ Return Hello Message """

        a_viewset = [
            'Uses Action (list, create, retrieve, update, partial_update)',
            'Automacally maps to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message':'Hello !', 'a_viewset':a_viewset})

    def create(self, request):
        """ create a new hello message """

        serializer = serializers.HelloSerializers(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)

            return Response({'message':message})
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None):
        """ Handles getting an object by its ID """

        return Response({'http_method':'GET'})

    def update(self, request, pk = None):
        """ Handles updating an object """

        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk = None):
        """ handles updating part of an object """

        return Response({'http_method':'PATCH'})

    def destroy(self, request, pk = None):
        """ Handles removing an object """

        return Response({'http_method':'delete'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handles creating, reading and updating profiles """

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)


class LoginViewSet(viewsets.ViewSet):
    """ check email and password and return an auth token """

    serializer_class = AuthTokenSerializer

    def create(self,request):
        """ use the ObtainAuthToken APIView to validate and create token """

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Handles creating, reading and updating profile feed items. """

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """ SET the user Profile to the logged in user """

        serializer.save(user_profile= self.request.user)
