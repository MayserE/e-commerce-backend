from datetime import datetime

from django.utils.timezone import make_aware
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=128,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        now = make_aware(datetime.now())
        validated_data['created_at'] = now
        validated_data['updated_at'] = now
        return super().create(validated_data)
