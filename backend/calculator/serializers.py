from rest_framework import serializers
from .models import CarbonCalculation

class CarbonCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonCalculation
        fields = '__all__'
        read_only_fields = ('predicted_emission',)