from rest_framework import generics
from rest_framework.permissions import AllowAny

from branch_office_products.models import BranchOfficeProduct
from branch_office_products.serializers import BranchOfficeProductSerializer


class GetBranchOfficeProductsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = BranchOfficeProduct.objects.select_related('branch_office', 'product__category').prefetch_related(
        'product__product_images')
    serializer_class = BranchOfficeProductSerializer
