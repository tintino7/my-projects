
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("page<int:page_id><str:page_name>", views.page, name="page"),
    path("user<str:user_name>",views.user, name="user"),
    path("edit", views.edit_post, name="edit_post"),
    path("like", views.like, name="like")    
]
