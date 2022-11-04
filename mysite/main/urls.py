from django.urls import path
from .views import (
    homepage_view,
    create_list_view,
    view_lists_view,
    view_list_view)

app_name = 'main'
urlpatterns = [
    path("", homepage_view, name="homepage-view"),
    path("create/", create_list_view, name="create-list-view"),
    path("view/", view_lists_view, name="view-lists-view"),
    path("view/<int:id>", view_list_view, name="view-list-view"),
]