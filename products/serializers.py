from datetime import datetime

from rest_framework import serializers

from categories.models import Category
from categories.serializers import CategorySerializer
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


class CreateProductSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'category', 'created_at', 'updated_at']

    def create(self, validated_data):
        try:
            category = Category.objects.get(id=validated_data['category_id'])
        except Category.DoesNotExist:
            raise serializers.ValidationError('La categoría no existe.')

        product = Product(
            category=category,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=validated_data['name'],
            detail=validated_data['detail'],
            price=validated_data['price']
        )
        product.save()
        return product
