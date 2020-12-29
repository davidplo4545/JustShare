import os
from django.conf import settings
from .models import CustomUser, Photo, Collection, UserProfile
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
)

# from .permissions import IsUserProfile, IsReaderOrReadOnly, IsEntryOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by("date_joined")
    serializer_class = UserSerializer
    http_method_names = ["get"]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
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
    http_method_names = ["get", "post", "delete", "patch"]

    def get_queryset(self):
        # print(UserProfile.objects.get(user__pk=user_pk))
        friends = UserProfile.objects.get(user__pk=self.kwargs["user_pk"]).friends()
        return friends

    def retrieve(self, request, pk=None, user_pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, user_pk=None):
        try:
            friends_queryset = self.get_queryset()
        except:
            return Response({"status": "User does not exist"})
        serializer = self.serializer_class(friends_queryset, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        friend = CustomUser.objects.get(id=self.kwargs.get("user_pk"))
        serializer.save(creator=self.request.user, friend=friend, status=0)


class PhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoints that allows the user to view/create/delete photos.
    """

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get", "post", "delete", "patch"]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

    def perform_update(self, serializer):
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


# class PublicBookEntryViewSet(viewsets.ModelViewSet):
#     serializer_class = BookEntrySerializer
#     queryset = BookEntry.objects.all()
#     permission_classes = [permissions.IsAuthenticated, IsEntryOwnerOrReadOnly]

#     def get_serializer_class(self):
#         if self.action in ['create']:
#             return BookEntryCreateSerializer
#         return BookEntrySerializer

#     def get_queryset(self):
#         return BookEntry.objects.filter(reader__pk=self.kwargs['profile_pk'])

#     def create(self, request,  pk=None, profile_pk=None):
#         serializer = self.get_serializer_class()(data=request.data)
#         reader = Profile.objects.get(id=profile_pk)
#         # probably not a neccessary check
#         if reader != request.user.profile:
#             raise serializers.ValidationError(
#                 {'error': 'cannot post to a different profile'})
#         book_id = request.data['book']
#         if serializer.is_valid():
#             # check if entry with this book already exists
#             if reader.entries.filter(book__id=book_id).exists():
#                 raise serializers.ValidationError(
#                     {'error': 'You have already added entry for this book.'})
#             self.perform_create(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# class PrivateBookEntryViewSet(viewsets.ModelViewSet):
#     serializer_class = BookEntrySerializer
#     permission_classes = [
#         permissions.IsAuthenticated, IsReaderOrReadOnly]

#     def get_queryset(self):
#         """ Return a queryset of the current user book entries"""
#         reader = self.request.user.profile
#         return BookEntry.objects.filter(reader=reader)

#     def get_serializer_class(self):
#         if self.action in ['create']:
#             return BookEntryCreateSerializer
#         return BookEntrySerializer

#     def create(self, request,  *args, **kwargs):
#         serializer = self.get_serializer_class()(data=request.data)
#         reader = request.user.profile
#         book_id = request.data['book']
#         if serializer.is_valid():
#             # check if entry with this book already exists
#             if reader.entries.filter(book__id=book_id).exists():
#                 raise Response(
#                     {'error': 'You have already added entry for this book.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#             self.perform_create(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def perform_create(self, serializer):
#         serializer.save(reader=self.request.user.profile)

#     def update(self, request, pk=None, *args, **kwargs):
#         entry = self.get_object()
#         entry_data = request.data.copy()
#         entry_data['entry'] = entry
#         serializer = self.serializer_class(
#             entry, data=entry_data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self,  request, pk=None):
#         entry = self.get_object()
#         entry.delete()
#         return Response({'status': 'successfuly deleted the entry'}, status=status.HTTP_200_OK)


# class ReadingRecordViewSet(viewsets.ModelViewSet):
#     serializer_class = ReadingRecordSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         entry_pk = self.kwargs['entry_pk']
#         return ReadingRecord.objects.filter(book_entry__id=entry_pk)

#     def create(self, request, entry_pk, *args, **kwargs):
#         entry = BookEntry.objects.get(pk=entry_pk)
#         record_data = request.data.copy()
#         record_data['book_entry'] = entry
#         serializer = self.serializer_class(data=record_data)
#         if serializer.is_valid():
#             serializer.save(book_entry=entry)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, entry_pk, pk=None):
#         record = self.get_object()
#         entry = record.book_entry
#         # can only delete the last record
#         if self.is_last_record(entry, record):
#             record.delete()
#             try:
#                 entry.current_page = list(
#                     entry.reading_records.all())[-2].current_page
#             except:
#                 entry.current_page = 0
#             entry.save()
#             return Response({'status': 'successfuly deleted the record'}, status=status.HTTP_200_OK)
#         return Response({'error': 'can only delete the last record of the entry.'}, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, entry_pk, pk=None, *args, **kwargs):
#         record = ReadingRecord.objects.get(pk=pk)
#         entry = record.book_entry
#         record_data = request.data.copy()
#         record_data['book_entry'] = entry
#         record_data['current_record_id'] = record.pk
#         # can only update the last record
#         if self.is_last_record(entry, record):
#             serializer = self.serializer_class(
#                 record, data=record_data, partial=True)
#             if serializer.is_valid():
#                 serializer.save(book_entry=entry)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'error': 'can only update the last record of the entry.'}, status=status.HTTP_400_BAD_REQUEST)

#     def is_last_record(self, entry, record):
#         """
#         Check if the record is the last record in the entry
#         """
#         last_record = list(entry.reading_records.all())[-1]
#         return last_record == record
