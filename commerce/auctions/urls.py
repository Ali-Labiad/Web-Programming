from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/comment/<int:listing_id>", views.addcomment, name="addcomment"),
    path("listing/bid/<int:listing_id>", views.addbid, name="addbid"),
    path("listing/addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/closelisting/<int:listing_id>", views.closelisting, name="closelisting"),
    path("categorylist", views.categorylist, name="categorylist"),
    path("categorylist/listing/<str:name>", views.categorylisting, name="categorylisting")
]
