from django.contrib import admin

from .models import Cart,CartItem,Category,OrderItem,Order,Product,ProductImage

models = [Cart,CartItem,Category,OrderItem,Order,Product,ProductImage]

for model in models:

    admin.site.register(model)

    