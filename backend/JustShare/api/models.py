from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email


def get_image_path(instance, filename):
    return "/".join(["images", str(instance.uploader.id), filename])


class Photo(models.Model):
    # SETUP MEDIA
    uploader = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to=get_image_path)
    upload_date = models.DateField(auto_now_add=True)

    # add creation_date later !


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    thumbnail = models.ImageField(blank=True)
    members = models.ManyToManyField(CustomUser, related_name="collections")
    photos = models.ManyToManyField(Photo, related_name="collections")