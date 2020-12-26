from rest_framework import serializers
from .models import CustomUser, UserProfile, Photo, Collection


class ProfileCreationSerializer(viewsets.ModelViewSet):
   class Meta:
       model = UserProfile
       fields = [
       'email',
       'password',
       'first_name',
       'last_name'
       ]
       extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # create user 
        user = CustomUser.objects.create(
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        
        profile_data = validated_data.pop('profile')
        # create profile
        profile = Profile.objects.create(
            user = user
            first_name = profile_data['first_name'],
            last_name = profile_data['last_name'],
            # etc...
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "date_joined", "is_superuser", "profile"]

 
    def create(self, validated_data):
        # create user 
        user = User.objects.create(
            url = validated_data['url'],
            email = validated_data['email'],
            # etc ...
        )

        profile_data = validated_data.pop('profile')
        # create profile
        profile = Profile.objects.create(
            user = user
            first_name = profile_data['first_name'],
            last_name = profile_data['last_name'],
            # etc...
        )

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class PhotoSerializer(serializers.ModelSerializer):
    uploader = UserSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"
