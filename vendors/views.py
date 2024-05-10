from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from VendorManagement.renderers import VendorManagementRenderer
from .models import *
from rest_framework import generics, permissions
import requests
from rest_framework import status

class VendorListCreate(generics.ListCreateAPIView):
    serializer_class = VendorSerializer
    renderer_classes = [VendorManagementRenderer,]
    queryset=Vendor.objects.all()

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=VendorSerializer
    renderer_classes = [VendorManagementRenderer,]
    queryset=Vendor.objects.all()
    lookup_field='id'

class VendorPerformace(generics.ListAPIView):
    serializer_class=HistoricalPerformanceSerializer       
    renderer_classes = [VendorManagementRenderer,]
    queryset=HistoricalPerformance.objects.all()
    lookup_field='id'
