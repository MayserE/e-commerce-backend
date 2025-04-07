from django.urls import path

from branch_office_products.views import BranchOfficeProductListView

urlpatterns = [
    path('', BranchOfficeProductListView.as_view(), name='branch_office_product_list')
]
