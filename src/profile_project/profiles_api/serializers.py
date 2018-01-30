from rest_framework import serializers


# create your class here

class HelloSerializers(serializers.Serializer):
    """ serializers a name field for testing API """

    name = serializers.CharField(max_length=10)
    
