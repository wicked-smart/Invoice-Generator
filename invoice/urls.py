from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index, name="index" ),
    path("items", views.invoice_items, name="items"),
    path("purchase_items", views.purchase_items, name="bought_items"),
    path("update_purchase_items/<str:invoice_id>", views.update_purchase_items, name="update_bought_items")
]

