from datetime import datetime

from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        category = Category(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=validated_data['name']
        )
        category.save()
        return category
