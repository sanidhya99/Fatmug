from .views import *

from django.urls import path

urlpatterns = [
    path("", PurchaseOrderListCreate.as_view(), name="purchase_list_create"),
    path("<int:id>/", PurchaseRetrieveUpdateDestroy.as_view(), name="purchase_retrieve_update_destroy"),
    path("<int:id>/acknowledge", VendorAcknowledgement.as_view(), name="purchase_acknowledge"),
    
]
