from django.urls import path

from shopping_carts.views import GetOrCreateShoppingCartView

urlpatterns = [
    path('', GetOrCreateShoppingCartView.as_view(), name='Get_Or_Create_ShoppingCart')

]