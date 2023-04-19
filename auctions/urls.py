from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new_listing", views.create_new_listing, name="create_new_listing"),
    path("<int:listing_id>/post_listing", views.listing, name="post_listing"),
    path("<int:listing_id>/get_listing", views.get_listing, name="get_listing"),
    path("<int:listing_id>/commend", views.commend, name="add_comment"),
    path("<int:listing_id>/rm", views.add_watchlist, name="add_watchlist"),
    path("<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("<int:listing_id>/close", views.close_bid, name="close_bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("<str:category>/category", views.category, name="category")

]
