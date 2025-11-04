from django.urls import path
from community_app.views import*

urlpatterns = [
    path("community_home/",community_home, name="community_home"),
    path("post/new/",create_post, name="create_post"),
    path("post/<int:post_id>/",post_detail, name="post_detail"),
]
