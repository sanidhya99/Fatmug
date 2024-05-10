from rest_framework import serializers
from .models import Vendor,HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['on_time_delivery_rate', 'quality_rating_avg','average_response_time','fulfillment_rate']
