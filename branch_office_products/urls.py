from django.urls import path

from branch_office_products.views import GetBranchOfficeProductsView

urlpatterns = [
    path('', GetBranchOfficeProductsView.as_view(), name='branch_office_product_list')
]
