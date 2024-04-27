from django.urls import path
from .views import home,details,shop

urlpatterns = [
    path('',home,name="home"),
    path('shop/details',details,name="shop-details"),
    path('shop/',shop,name="shop"),
]
