"""JustShare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

# from rest_framework_nested import routers
from api import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(r"users", views.UserViewSet)
router.register(r"profiles", views.ProfileViewSet)
router.register(r"", views.AuthenticationViewSet)
router.register(r"collections", views.CollectionViewSet, basename="Collection")
router.register(r"photos", views.PhotoViewSet)

users_router = routers.NestedSimpleRouter(router, r"users", lookup="user")
# users router for /profiles
users_router.register(r"friends", views.FriendshipViewSet, basename="user-friends")

urlpatterns = [
    path("admin/", admin.site.urls),
    # url(r"^api/", include("rest_auth.urls")),
    path("api/invites/", views.CollectionInvitesView.as_view()),
    path("api/", include(router.urls)),
    path("api/", include(users_router.urls)),
    path("api/people", views.FriendsList.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)