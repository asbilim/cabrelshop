from django.urls import path
from .views import home,details,shop,signin,signup,signout

urlpatterns = [
    path('',home,name="home"),
    path('shop/details/<str:slug>',details,name="shop-details"),
    path('shop/',shop,name="shop"),
    path('signin',signin,name="signin"),
    path('signup',signup,name="signup"),
    path('signout',signout,name="signout"),
]
