from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


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

    def friends(self):
        return Friendship.objects.filter(Q(creator=self.user) | Q(friend=self.user))

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Friendship(models.Model):
    PENDING = "PENDING"
    DONE = "DONE"
    STATUS_CHOICES = (
        (PENDING, "PENDING"),
        (DONE, "DONE"),
    )
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
    # SETUP MEDIA
    uploader = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to=get_image_path)
    upload_date = models.DateField(auto_now_add=True, editable=False)

    # add creation_date later !


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    thumbnail = models.ImageField(blank=True)
    members = models.ManyToManyField(CustomUser, related_name="collections")
    photos = models.ManyToManyField(Photo, related_name="collections")