from rest_framework import serializers
from rest_framework.validators import ValidationError
from invoice.models  import *

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"

class BoughtItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoughtItem
        fields = "__all__"

    def validate(self, data):
        
        item = data.get('item')

        try: 
            Item.objects.get(id=item)
        except Item.DoesNotExist:
            raise ValidationError(f"Item no. {item} Does not exsist!")
        
        quantity = data.get('quantity')

        if quantity > item.quantity:
            raise ValidationError("Bought Item Quantity is greater than available item quantity!!")
        
        return data

class InvoiceItemSerializer(serializers.ModelSerializer):
    items = BoughtItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ["id", "items", "created_at", "updated_at"]
        extra_kwargs = {
            "created_at": {"required": False},
            "updated_at": {"required": False},
            "id": {"required": False}
        }


    def to_internal_value(self, data):
        # Modify the incoming data structure to match the expected format
        print("invoce data :- ", data)
        modified_data = {"items": data}
        return super().to_internal_value(modified_data)
    

    def create(self, validated_data):
        print("validated_data := ", validated_data)
        bought_items_data = validated_data.pop('items')
        print("bought items data := ", bought_items_data)

        # Assuming you already have the BoughtItem instances
        bought_items = [BoughtItem.objects.create(**item_data) for item_data in bought_items_data]
        print(bought_items)
        #upadte items quantity
        for bar in bought_items_data:
            foo = bar["item"]
            foo.quantity -= bar["quantity"]
            foo.save()

        # Create Invoice instance
        invoice = Invoice.objects.create(**validated_data)
        for item in bought_items:
            invoice.items.add(item)
        invoice.save()

        return invoice
