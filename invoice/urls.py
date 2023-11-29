from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index, name="index" ),
    path("items", views.invoice_items, name="items"),
    path("purchase_items", views.purchase_items, name="bought_items")
]