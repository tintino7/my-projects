from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.entry_search, name="entry_search"),
    path("newpage", views.new_page, name="new_page"),
    path("editpage", views.edit_page, name="edit_page"),    
    path("randompage", views.random_page, name="random_page"),
    path("<str:title>", views.entry, name="entry")
]