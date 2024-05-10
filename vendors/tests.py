from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor

class VendorAPITestCase(TestCase):
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

    def test_create_vendor(self):
        response = self.client.post('/vendors/', self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)  # Assuming one vendor is created in setUp

    # Add more test cases for other endpoints (retrieve, update, delete, etc.) as needed
