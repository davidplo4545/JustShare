from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser, UserProfile, Photo, Collection
from rest_framework.authentication import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "date_joined", "is_superuser", "profile"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        # create user
        user = CustomUser.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        # create profile
        profile = UserProfile.objects.create(
            user=user,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
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
