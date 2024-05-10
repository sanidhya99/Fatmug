from .views import *

from django.urls import path

urlpatterns = [
    path("", VendorListCreate.as_view(), name="vendor_list_create"),
    path("<int:id>/", VendorRetrieveUpdateDestroy.as_view(), name="vendor_retrieve_update_destroy"),
    path("<int:id>/performance", VendorPerformace.as_view(), name="vendor_performance"),
]
