from django.contrib import admin
from .models import CustomUser, Photo, Collection

admin.site.register(CustomUser)
admin.site.register(Photo)
admin.site.register(Collection)
