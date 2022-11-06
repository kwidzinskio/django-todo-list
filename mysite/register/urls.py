from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (register_view,
                    profile_view,
                    )

app_name = 'register'
urlpatterns = [
    path('register/', register_view, name="register-view"),
    path("profile/", profile_view, name="profile-view"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)