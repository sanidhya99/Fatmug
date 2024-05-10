from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import PurchaseOrder
from vendors.models import *

class PurchaseOrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': '1234567890',
            'address': 'Test Address',
            'vendor_code': 'V001'
            # Add more fields as needed
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

        self.purchase_order_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'order_date': '2024-05-10T12:00:00Z',
            'expected_delivery_date': '2024-05-15T12:00:00Z',
            'delivery_date': '2024-05-15T12:00:00Z',
            'items': {'item1': 'description1', 'item2': 'description2'},
            'quantity': 10,
            'status': 'completed'
            # Add more fields as needed
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.purchase_order_data)

    def test_create_purchase_order(self):
        response = self.client.post('/purchase_orders/', self.purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)  # Assuming one purchase order is created in setUp

    # Add more test cases for other endpoints (retrieve, update, delete, etc.) as needed
