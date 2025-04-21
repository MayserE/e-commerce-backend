from django.urls import path

from shopping_carts.views import GetCurrentShoppingCartView, AddShoppingCartProductView

urlpatterns = [
    path('current/', GetCurrentShoppingCartView.as_view(), name='current_shopping_cart'),
    path('', AddShoppingCartProductView.as_view(), name='shopping_cart_product_adding'),

]
