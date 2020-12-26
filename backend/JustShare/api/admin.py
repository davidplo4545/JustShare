from django.contrib import admin
from .models import CustomUser, Profile, Photo, Collection

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Collection)
