from django.urls import path
from .views import home,details,shop,signin,signup,signout,add_to_cart,cart_items_view, add_to_cart, update_cart_item, remove_cart_item

urlpatterns = [
    path('',home,name="home"),
    path('shop/details/<str:slug>',details,name="shop-details"),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/items/', cart_items_view, name='cart_items_view'),
    path('cart/item/update/<int:item_id>/<str:action>/', update_cart_item, name='update_cart_item'),
    path('cart/item/remove/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('shop/',shop,name="shop"),
    path('signin',signin,name="signin"),
    path('signup',signup,name="signup"),
    path('signout',signout,name="signout"),
]
