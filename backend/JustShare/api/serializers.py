from itertools import chain
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import (
    CustomUser,
    UserProfile,
    Friendship,
    Photo,
    Collection,
    CollectionInvite,
    STATUS_CHOICES,
)
from rest_framework.authentication import authenticate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "last_name"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ["url", "email", "date_joined", "profile"]

    # - MABYE ADD LATER
    def to_representation(self, instance):
        result_json = super(UserSerializer, self).to_representation(instance)
        # result_json["friends"] = []

        # for friendship in instance.profile.friendships():
        #     friendship_data = FriendshipSerializer(
        #         friendship,
        #         context={
        #             "request": self.context["request"],
        #             "current_user_id": instance.id,
        #         },
        #     )
        #     result_json["friends"].append(friendship_data.data)
        return result_json


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

    def to_representation(self, instance):
        result_json = super(FriendshipSerializer, self).to_representation(instance)
        user_id = self.context["current_user_id"]
        friend = result_json.pop("friend")
        creator = result_json.pop("creator")
        # setting the 'friend' key to be different from the
        # authenticated user, remove 'creator key
        if str(user_id) == str(creator):
            friend_user_object = CustomUser.objects.get(id=friend)
            serializer = UserSerializer(
                friend_user_object, context={"request": self.context["request"]}
            )
        else:
            friend_user_object = CustomUser.objects.get(id=creator)
            serializer = UserSerializer(
                friend_user_object, context={"request": self.context["request"]}
            )

        result_json.update({"friend": serializer.data})
        return result_json

    #     result_json["friends"] = []

    #     for friendship in instance.profile.friendships():
    #         friendship_data = FriendshipSerializer(friendship)
    #         result_json["friends"].append(friendship_data.data)
    #     return result_json


class FriendStatusSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    friendship_status = serializers.CharField(read_only=True)


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

    class Meta:
        model = Collection
        fields = "__all__"

        extra_kwargs = {
            "members": {"read_only": True},
            "creator": {"read_only": True},
            "photos": {"read_only": True},
        }


class UpdateCollectionPhotosSerializer(serializers.ModelSerializer):
    photos_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Photo.objects.all(),
        source="photos",
        required=False,
    )

    class Meta:
        model = Collection
        fields = ["photos_ids"]

    def validate(self, data):
        """
        Check that the photos were uploaded by the requesting user
        """
        user = self.context["request"].user
        photos = data["photos"]
        for photo in photos:
            if photo.uploader != user:
                raise serializers.ValidationError(
                    {"photos_ids": "invalid photos ids submitted"}
                )
        return data

    def update(self, instance, validated_data):
        """
        Add/Delete photos from collection according to request action
        """
        photos = validated_data.pop("photos")
        if self.context["action"] == "add_photos":
            for photo in photos:
                if photo not in instance.photos.all():
                    instance.photos.add(photo)
        elif self.context["action"] == "delete_photos":
            for photo in photos:
                if photo in instance.photos.all():
                    instance.photos.remove(photo)
        instance.save()

        return instance


class CollectionInviteSendSerializer(serializers.ModelSerializer):
    to_user = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = CollectionInvite
        fields = "__all__"
        extra_kwargs = {
            "collection": {"read_only": True},
            "from_user": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def validate(self, data):
        """
        Check that an invite hasn't been sent/accepted already
        """
        user = self.context["request"].user
        collection = self.context["collection"]

        invites = CollectionInvite.objects.filter(to_user=data["to_user"])
        if invites:
            raise serializers.ValidationError(
                {"error": "An invite has already been sent/accepted"}
            )
        return data

    def create(self, validated_data):
        # get the collection from the View
        collection = self.context["collection"]
        collection_invite = CollectionInvite.objects.create(
            collection=collection,
            from_user=self.context["request"].user,
            to_user=validated_data["to_user"],
            status="PENDING",
        )
        collection_invite.save()
        return collection_invite


class CollectionInviteReplySerializer(serializers.ModelSerializer):
    ACCEPT = "ACCEPT"
    DECLINE = "DECLINE"
    ACTION_CHOICES = (
        (ACCEPT, "ACCEPT"),
        (DECLINE, "DECLINE"),
    )
    action = serializers.ChoiceField(choices=ACTION_CHOICES, required=True)

    class Meta:
        model = CollectionInvite
        fields = ["action"]

    def update(self, instance, validated_data):
        collection = self.context["collection"]
        collection.members.add(self.context["request"].user)
        instance.status = "DONE"
        instance.save()
        return instance


class CollectionInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionInvite
        fields = "__all__"
