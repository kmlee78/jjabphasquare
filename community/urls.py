from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.post_list, name="post-list"),
    path("detail/", views.post_detail, name="post-detail"),
    path("create/", views.post_create, name="post-create"),
    path("detail/<int:post_id>/edit", views.post_edit, name="post-edit"),
    path("detail/<int:post_id>/delete", views.post_delete, name="post-delete"),
]
