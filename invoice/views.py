from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from invoice.serializers.serializer import *
from .models import *


# Create your views here.
@api_view(['GET'])
def index(request):
    return Response({"message": "Helath check: working..."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def invoice_items(request):

    if request.method == 'GET':

        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', 'PUT'])
def purchase_items(request):

    if request.method == 'POST':

        data = request.data
        foo = data
        serializer = BoughtItemSerializer(data=data, many=True)

        if serializer.is_valid():

            invoice = InvoiceItemSerializer(data=foo)
            if invoice.is_valid():
                invoice.save()
                return Response(invoice.data , status=status.HTTP_200_OK)
            else:
                return Response(invoice.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def update_purchase_items(request, invoice_id):
    
    if request.method == 'PUT':

        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
             return Response({"message": f"Invoice with id {invoice_id} does not exists!"})

        if invoice.pdf_generated == True:
            return Response({"message": "Purchase cannot be updated now as Invoice PDF has been generated!"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data

        serializer = BoughtItemSerializer(data=data, many=True)

        if serializer.is_valid():
            invoice = InvoiceItemSerializer(invoice, data=data, partial=True)

            if invoice.is_valid():
                invoice.save()
                return Response(invoice.data, status=status.HTTP_200_OK)
            else:
                return Response(invoice.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    else:
        return Response({"message": "not working"})