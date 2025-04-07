from rest_framework import serializers

from branch_office_products.models import BranchOfficeProduct
from branch_offices.serializers import BranchOfficeSerializer
from products.serializer import ProductSerializer


class BranchOfficeProductSerializer(serializers.ModelSerializer):
    branch_office = BranchOfficeSerializer()
    product = ProductSerializer()

    class Meta:
        model = BranchOfficeProduct
        fields = '__all__'
