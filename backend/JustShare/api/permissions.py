from rest_framework import permissions


class FriendshipPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        # Deny 'delete' action if user does not belong to the object
        if view.action == "destroy":
            return obj.friend == request.user or obj.creator == request.user
        elif view.action in ["retrieve", "create"]:
            return True
        else:
            return False