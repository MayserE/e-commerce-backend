from rest_framework import serializers

from branch_offices.models import BranchOffice


class BranchOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchOffice
        fields = '__all__'