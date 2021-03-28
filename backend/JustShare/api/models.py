from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

PENDING = "PENDING"
DONE = "DONE"

STATUS_CHOICES = (
    (PENDING, "PENDING"),
    (DONE, "DONE"),
)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=120, blank=False)
    last_name = models.CharField(max_length=120, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def friendships(self):
        return Friendship.objects.filter(
            Q(creator=self.user) | Q(friend=self.user)
        ).order_by("-status")

    def friends(self):
        """
        Returns a list of dictionaries containing the user's friend and
        their friendship status (Currently showing all other users as well)
        Format:
        [
            {"user":user,"friendship_status":friendship_status},
            {"user":user,"friendship_status":friendship_status}
        ]
        """
        result_friends = []
        friendships = self.friendships().order_by("-status")
        # remove the requesting user from the list
        friends_ids = [self.user.id]
        for friendship in list(friendships):
            # 'friend' is different from the user that sent the request
            friend = (
                friendship.creator
                if friendship.creator != self.user
                else friendship.friend
            )
            friends_ids.append(friend.id)
            result_friends.append(
                {"user": friend, "friendship_status": friendship.status}
            )
        other_users = CustomUser.objects.exclude(id__in=friends_ids)
        for user in other_users:
            result_friends.append({"user": user, "friendship_status": "NONE"})

        return result_friends

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        CustomUser, related_name="friendship_creater", on_delete=models.CASCADE
    )
    friend = models.ForeignKey(
        CustomUser, related_name="friend", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"-{self.creator.profile.get_full_name()}- friends with -{self.friend.profile.get_full_name()}-"


def get_image_path(instance, filename):
    return "/".join(["images", str(instance.uploader.id), filename])


class Photo(models.Model):
    uploader = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to=get_image_path)
    upload_date = models.DateField(auto_now_add=True, editable=False)


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    thumbnail = models.ImageField(blank=True)
    creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_collections"
    )
    members = models.ManyToManyField(CustomUser, related_name="collections")
    photos = models.ManyToManyField(Photo, related_name="collections")

    def __str__(self):
        return f"Collection: {self.name}"


class CollectionInvite(models.Model):
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name="invites"
    )
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="invites_sent"
    )
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="invites_received"
    )
    created_at = models.DateField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"Collection Invite: from {self.from_user} to {self.to_user}"
