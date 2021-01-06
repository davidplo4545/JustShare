from itertools import chain
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser, UserProfile, Friendship, Photo, Collection
from rest_framework.authentication import authenticate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "last_name"]


class FriendshipSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    friend = serializers.PrimaryKeyRelatedField(read_only=True)
    # status = serializers.ChoiceField(choices=Friendship.STATUS_CHOICES)

    def __init__(self, *args, **kwargs):
        """ Set all fields to read_only=True """
        super(FriendshipSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].read_only = True

    class Meta:
        model = Friendship
        fields = ["id", "creator", "friend", "status"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ["url", "email", "date_joined", "profile"]

    def to_representation(self, instance):
        result_json = super(UserSerializer, self).to_representation(instance)
        result_json["friends"] = []

        for friendship in instance.profile.friends():
            friendship_data = FriendshipSerializer(friendship)
            result_json["friends"].append(friendship_data.data)
            # result_json["friends"].append(
            #     {
            #         "creator": friendship.creator.id,
            #         "friend": friendship.friend.id,
            #         "status": friendship.status,
            #     }
            # )
        return result_json


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "profile"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        # create user
        user = CustomUser.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        profile_data = validated_data.pop("profile")
        # create profile
        profile = UserProfile.objects.create(
            user=user,
            first_name=profile_data["first_name"],
            last_name=profile_data["last_name"],
        )
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if user:
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError(
                "Unable to login with credentials provided."
            )


class PhotoSerializer(serializers.ModelSerializer):
    uploader = ProfileSerializer(source="uploader.profile", read_only=True)

    class Meta:
        model = Photo
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)
    # photos_ids = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=False,
    #     queryset=Photo.objects.all(),
    #     source="photos",
    #     required=False,
    # )

    class Meta:
        model = Collection
        fields = [
            "id",
            "thumbnail",
            "name",
            "description",
            "members",
            "photos",
            "creator",
        ]

        extra_kwargs = {
            "members": {"read_only": True},
            "creator": {"read_only": True},
            "photos": {"read_only": True},
        }

    def update(self, instance, validated_data):
        # check for photos to upload
        try:
            photos_ids = self.initial_data["photos_ids"]
            photos = Photo.objects.filter(pk__in=photos_ids)
            for photo in photos:
                instance.photos.add(photo)
        except Exception as e:
            print(e)
            instance.name = validated_data.get("name")
            instance.description = validated_data.get("description")
            instance.thumbnail = validated_data.get("thumbnail")

        instance.save()
        return instance
