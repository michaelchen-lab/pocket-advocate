from django.urls import path, include
from rest_framework import routers

from . import views
from .api import ProfileView

router = routers.SimpleRouter()
router.register("profile", ProfileView, "profile")

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile_view, name="profile"),
    
    ## Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    ## API
    path("api/", include(router.urls))
]