from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json
from vendors.models import *
from .models import PurchaseOrder

class PurchaseOrderAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor_url = reverse('vendor-list')

    def test_create_vendor(self):
        # Test creating a new vendor
        data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test St',
            'vendor_code': 'TEST001'
        }
        response = self.client.post(self.vendor_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_vendors(self):
        # Test retrieving a list of vendors
        response = self.client.get(self.vendor_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add more test methods for other endpoints...

class PurchaseOrderModelTests(TestCase):
    def test_create_purchase_order(self):
        # Test creating a new purchase order
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St', vendor_code='TEST001')
        purchase_order = PurchaseOrder.objects.create(vendor=vendor, po_number='PO001', quantity=10, status='pending')
        self.assertEqual(purchase_order.po_number, 'PO001')
        self.assertEqual(purchase_order.quantity, 10)
        self.assertEqual(purchase_order.status, 'pending')

    # Add more test methods for other models and functionalities...
