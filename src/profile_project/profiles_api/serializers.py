from rest_framework import serializers

from . import models

# create your class here

class HelloSerializers(serializers.Serializer):
    """ serializers a name field for testing API """

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """ a serializer for our user profile objects """

    class Meta:
        # assign model
        model = models.UserProfile
        # what field will be used
        fields = ('id','email','name','password')
        # pastikan password write only
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ create and return a new user """

        user = models.UserProfile(
            email = validated_data['email'],
            name = validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
        
