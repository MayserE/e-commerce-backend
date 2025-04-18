from django.urls import path

from products.views import CreateProductView

urlpatterns = [
    path('', CreateProductView.as_view(), name='product_creation'),
]
