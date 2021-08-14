from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories_view, name="categories"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("createlisting", views.create_listing_view, name="createlisting"),
    path("mybids", views.mybids_view, name="mybids"),
    path("mylistings", views.mylisting_view, name="mylistings"),
    path("category/<str:category>", views.category_view, name="category"),
    path("item/<int:itemid>", views.item_view , name="item"),
    path("item/<int:itemid>/addtowatchlist", views.addtowatchlist_view , name="addtowatchlist"),
    path("item/<int:itemid>/bid/", views.bid_view , name="bid"),

]
