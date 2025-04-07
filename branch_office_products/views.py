from rest_framework import generics

from branch_office_products.models import BranchOfficeProduct
from branch_office_products.serializers import BranchOfficeProductSerializer


class BranchOfficeProductListView(generics.ListAPIView):
    queryset = BranchOfficeProduct.objects.select_related('branch_office', 'product__category').prefetch_related(
        'product__product_images')
    serializer_class = BranchOfficeProductSerializer
