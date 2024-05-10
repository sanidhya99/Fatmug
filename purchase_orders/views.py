from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from VendorManagement.renderers import VendorManagementRenderer
from .models import *
from vendors.models import *
from rest_framework import generics, permissions, status
from django.utils import timezone
from django.db.models import F
from django.db.models import Count
from django.db.models import Sum
from django.db.models import Avg
from django.db.models import ExpressionWrapper, FloatField

class PurchaseOrderListCreate(generics.ListCreateAPIView):
    serializer_class = PurchaseOrderSerializer
    renderer_classes = [VendorManagementRenderer,]
    queryset = PurchaseOrder.objects.all()

class PurchaseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseOrderSerializer
    renderer_classes = [VendorManagementRenderer,]
    queryset = PurchaseOrder.objects.all()
    lookup_field = 'id'

    def calculate_fulfillment_rate(self, vendor):
        total_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
        completed_purchase_orders = total_purchase_orders.filter(status__iexact='completed')

        if total_purchase_orders.exists():
            return completed_purchase_orders.count() / total_purchase_orders.count() 
        else:
            return 0

    def calculate_on_time_delivery_rate(self, vendor):
        completed_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, status__iexact='completed')
        on_time_deliveries = completed_purchase_orders.filter(delivery_date__lte=F('expected_delivery_date'))

        if completed_purchase_orders.exists():
            return on_time_deliveries.count() / completed_purchase_orders.count() 
        else:
            return 0

    def put(self, request, *args, **kwargs):
        po_id = kwargs.get('id')

        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'detail': 'Purchase order not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(purchase_order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            vendor = purchase_order.vendor

            # Update quality rating average
            quality_rating = request.data.get('quality_rating')
            if quality_rating is not None:
                completed_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, status__iexact='completed')
                quality_ratings = [po.quality_rating for po in completed_purchase_orders if po.quality_rating is not None]
                quality_ratings.append(float(quality_rating))

                if quality_ratings:
                    quality_rating_avg = sum(quality_ratings) / len(quality_ratings)
                else:
                    quality_rating_avg = 0

                vendor.quality_rating_avg = quality_rating_avg
                vendor.save()

                historical_performance = HistoricalPerformance.objects.get(vendor=vendor)
                historical_performance.quality_rating_avg = quality_rating_avg
                historical_performance.save()

            # Update acknowledgment date and calculate average response time
            if 'status' in request.data:
                fulfillment_rate = self.calculate_fulfillment_rate(vendor)
                vendor.fulfillment_rate = fulfillment_rate
                vendor.save()

                historical_performance = HistoricalPerformance.objects.get(vendor=vendor)
                historical_performance.fulfillment_rate = fulfillment_rate
                historical_performance.save()
                status = request.data['status']
                if status.lower() == 'completed':
                    # Calculate and update on-time delivery rate
                    on_time_delivery_rate = self.calculate_on_time_delivery_rate(vendor)
                    vendor.on_time_delivery_rate = on_time_delivery_rate
                    vendor.save()
    
                    historical_performance.on_time_delivery_rate = on_time_delivery_rate
                    historical_performance.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorAcknowledgement(generics.CreateAPIView):
    serializer_class = PurchaseOrderSerializer
    renderer_classes = [VendorManagementRenderer,]

    def post(self, request, *args, **kwargs):
        po_id = self.kwargs.get('po_id')

        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'detail': 'Purchase order not found.'}, status=status.HTTP_404_NOT_FOUND)

        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        vendor = purchase_order.vendor

        vendor_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)

        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() / 3600 for po in vendor_purchase_orders]

        if response_times:
            average_response_time_hours = sum(response_times) / len(response_times)
        else:
            average_response_time_hours = 0

        vendor.average_response_time = average_response_time_hours
        vendor.save()

        historical_performance = HistoricalPerformance.objects.get(vendor=vendor)
        historical_performance.average_response_time = average_response_time_hours
        historical_performance.save()

        serializer = self.get_serializer(purchase_order)

        return Response(serializer.data, status=status.HTTP_200_OK)
