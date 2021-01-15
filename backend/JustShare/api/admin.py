from django.contrib import admin
from .models import (
    CustomUser,
    UserProfile,
    Photo,
    Collection,
    CollectionInvite,
    Friendship,
)

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Friendship)
admin.site.register(Photo)
admin.site.register(Collection)
admin.site.register(CollectionInvite)
