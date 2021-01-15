from rest_framework import permissions


class IsCollectionMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ["reply_invite", "list"]:
            return True
        elif view.action in ["partial_update", "update", "destroy"]:
            # only creator can edit the collection itself
            return obj.creator == request.user
        else:
            # only members can do "write" operations
            return request.user in obj.members.all()
        return False


class PhotoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Deny write actions if you are not the photo uploader
        if request.method not in permissions.SAFE_METHODS:
            return obj.uploader == request.user
        return True


class FriendshipPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Deny 'delete' action if user does not belong to the object
        if view.action == "destroy":
            return obj.friend == request.user or obj.creator == request.user
        elif view.action in ["retrieve", "create"]:
            return True
        else:
            return False