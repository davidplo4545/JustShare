from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser, UserProfile, Friendship, Photo, Collection
from rest_framework.authentication import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "date_joined", "is_superuser", "profile"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name"]


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


class FriendshipSerializer(serializers.ModelSerializer):
    creator = ProfileSerializer(read_only=True)
    friend = ProfileSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        """ Set all fields to read_only=True """
        super(FriendshipSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].read_only = True

    class Meta:
        model = Friendship
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
