import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import (
    CustomUser,
    UserProfile,
    Friendship,
    Photo,
    Collection,
    CollectionInvite,
    STATUS_CHOICES,
)
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets, serializers
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    FriendshipSerializer,
    RegisterSerializer,
    LoginSerializer,
    PhotoSerializer,
    CollectionSerializer,
    CollectionInvite,
    UpdateCollectionPhotosSerializer,
)

from .permissions import FriendshipPermission, PhotoPermission

# from .permissions import IsUserProfile, IsReaderOrReadOnly, IsEntryOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by("date_joined")
    serializer_class = UserSerializer
    http_method_names = ["get"]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     any_permission_actions = ['register', 'login']
    #     if self.action in any_permission_actions:
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]


class AuthenticationViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        if self.action == "login":
            return LoginSerializer
        elif self.action == "register":
            return RegisterSerializer
        elif self.action == "logout":
            return None
        return UserSerializer

    @action(detail=False, methods=["post"])
    def register(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user_id=user.id)
            response = {
                "email": user.email,
                "first_name": user.profile.first_name,
                "last_name": user.profile.last_name,
                "token": str(token),
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.validated_data["email"])
            token, created = Token.objects.get_or_create(user=user)
            response = {
                "email": user.email,
                "token": str(token),
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(
            {"error": "unable to login with provided credentials."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, methods=["get"])
    def logout(self, request):
        # deleting the token after logging out
        request.user.auth_token.delete()
        return Response({"status": "logout has been successfully initiated"})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by("user__date_joined")
    serializer_class = ProfileSerializer
    http_method_names = ["get"]


class FriendshipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendshipSerializer
    http_method_names = ["get", "post", "delete"]
    permission_classes = [FriendshipPermission]

    def get_queryset(self):
        return UserProfile.objects.get(user__pk=self.kwargs["user_pk"]).friends()

    def get_object(self):
        obj = get_object_or_404(Friendship, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, user_pk=None):
        try:
            friends_queryset = self.get_queryset()
        except:
            return Response(
                {"status": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(friends_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, pk=None, user_pk=None):
        try:
            friend = CustomUser.objects.get(id=user_pk)
        except:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        # can't "friend" yourself
        if friend == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # check if Friendship object exists already
        # change status to "DONE" if it does
        # create a new one if it doesn't exist
        try:
            friendship = Friendship.objects.get(
                friend=self.request.user, creator=friend
            )

            # disallow creating more than one friendship <-- PERMISSIONS
            if friendship.status == "DONE":
                return Response(
                    {"status": "friendship has already been created"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            friendship.status = "DONE"
            friendship.save()
            return Response(
                {"status": "friendship status has been changed"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # check if you already sent a friend request <-- PERMISSIONS
            try:
                friendship = Friendship.objects.get(
                    creator=self.request.user, friend=friend
                )
                return Response(
                    {"status": "friend request has already been sent"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except:
                pass

            serializer = FriendshipSerializer(data={})
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """ Only called when new Friendship object is created """
        friend = CustomUser.objects.get(id=self.kwargs.get("user_pk"))
        serializer.save(
            creator=self.request.user,
            friend=friend,
            status="PENDING",
        )

    def destroy(self, request, pk=None, user_pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "friendship has been deleted"}, status=status.HTTP_200_OK
        )


class PhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoints that allows the user to view/create/delete photos.
    """

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [PhotoPermission]
    http_method_names = ["get", "post", "delete", "patch"]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

    def destroy(self, request, pk=None):
        photo = self.get_object()
        # delete the image file from the directory
        # strip and join the MEDIA image path
        image_url = photo.image.url.split("media")[1][1:]
        photo_path = "/".join([settings.MEDIA_ROOT.replace("\\", "/"), image_url])
        os.remove(photo_path)
        photo.delete()
        return Response(
            {"status": "successfuly deleted the photo"}, status=status.HTTP_200_OK
        )


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete", "patch"]

    def get_queryset(self):
        return Collection.objects.filter(members__id=self.request.user.id)

    def list(self, request):
        try:
            queryset = self.get_queryset()
        except:
            return Response(
                {"status": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def partial_update(self,request, pk=None):

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, members=[self.request.user])

    @action(detail=True, methods=["patch"])
    def add_photos(self, request, pk=None):
        obj = self.get_object()
        context = {"request": request, "action": self.action}
        serializer = UpdateCollectionPhotosSerializer(
            obj, data=request.data, partial=True, context=context
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"status": "Photos has been added"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def delete_photos(self, request, pk=None):
        obj = self.get_object()
        context = {"request": request, "action": self.action}
        serializer = UpdateCollectionPhotosSerializer(
            obj, data=request.data, partial=True, context=context
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"status": "Photos has been deleted"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def invite(self, request, pk=None):
        collection = self.get_object()
        context = {"request": request, "collection": collection}
        # choose which serializer
        if request.data:
            serializer = CollectionInviteSendSerializer(
                data=request.data, context=context
            )
        else:
            try:
                invite = CollectionInvite.objects.get(
                    collection=collection,
                    to_user=request.user,
                    status=STATUS_CHOICES.PENDING,
                )
            except:
                return Response(
                    {"error": "No invite found to this collection"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = CollectionInviteReplySerializer(
                data=request.data, context=context
            )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"status": "Collection invite has been sent"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def reply_invite(self, request, pk=None):
        collection = self.get_object()
        context = {"request": request, "collection": collection}


class AcceptCollectionInvite(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get", "post", "delete"]
