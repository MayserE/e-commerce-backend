from rest_framework import serializers

from categories.serializer import CategorySerializer
from products.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
