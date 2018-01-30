from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers

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

    def list(self, request):
        """ Return Hello Message """

        a_viewset = [
            'Uses Action (list, create, retrieve, update, partial_update)',
            'Automacally maps to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message':'Hello !', 'a_viewset':a_viewset})

        
