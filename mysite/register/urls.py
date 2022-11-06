from .views import (register_view,
                    profile_view,
                    )
from django.urls import path

app_name = 'register'
urlpatterns = [
    path('register/', register_view, name="register-view"),
    path("profile/", profile_view, name="profile-view"),
    ]