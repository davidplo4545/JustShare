from rest_framework import permissions


class CollectionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

        if view.action == "reply_invite":
            return True
        else:
            # get permission only if user is included in the collection members
            return request.user in obj.members.all()


class PhotoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

    def has_object_permission(self, request, view, obj):
        # Deny write actions if you are not the photo uploader
        if request.method not in permissions.SAFE_METHODS:
            return obj.uploader == request.user
        return True


class FriendshipPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

    def has_object_permission(self, request, view, obj):
        # Deny 'delete' action if user does not belong to the object
        if view.action == "destroy":
            return obj.friend == request.user or obj.creator == request.user
        elif view.action in ["retrieve", "create"]:
            return True
        else:
            return False