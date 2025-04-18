from django.urls import path

from shopping_cart_products.views import AddProductToShoppingCartView, GetProductFromShoppingCartView, \
    IncreaseTheQuantityOfProductView, DecreaseTheQuantityOfProductView, RemoveProductFromShoppingCartView, \
    UpdateQuantityOfProductView, ClearShoppingCartView

urlpatterns = [
    path('', AddProductToShoppingCartView.as_view(),
         name='add-product-to-shopping-cart'),
    path('shopping-cart-product-list/', GetProductFromShoppingCartView.as_view(), name='shopping_cart_product_list'),
    path('increase-product/<uuid:product_id>/', IncreaseTheQuantityOfProductView.as_view(), name='increase_product'),
    path('decrease-product/<uuid:product_id>/', DecreaseTheQuantityOfProductView.as_view(), name='decrease_product'),
    path('remove-product/<uuid:product_id>/', RemoveProductFromShoppingCartView.as_view(), name='remove_product'),
    path('update-quantity/<uuid:product_id>/', UpdateQuantityOfProductView.as_view(), name='update_quantity'),
    path('clear-shopping-cart/', ClearShoppingCartView.as_view(),
         name='clear_shopping_cart'),
]
