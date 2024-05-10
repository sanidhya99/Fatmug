from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, HistoricalPerformance

class VendorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_vendor_list_create(self):
        url = reverse('vendor_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # You can add more test cases to ensure correct behavior for POST requests to create vendors

    def test_vendor_retrieve_update_destroy(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact', address='Address', vendor_code='V001')
        url = reverse('vendor_retrieve_update_destroy', kwargs={'id': vendor.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # You can add more test cases to ensure correct behavior for updating and deleting vendors

    def test_vendor_performance(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact', address='Address', vendor_code='V001')
        url = reverse('vendor_performance', kwargs={'id': vendor.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # You can add more test cases to ensure correct behavior for vendor performance endpoint

    # Add more test cases as needed for your application
