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
            Item.objects.get(id=item.id)
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
    
    def update(self, instance, validated_data):
        existing_items = instance.items.all()
        #print("exsisting items := ", existing_items)
        #print("update validated data := ", validated_data)

        items = validated_data.get("items", [])


        # Update quantities for existing items
        for existing_item in existing_items:
            for updated_item_data in validated_data.get('items', []):
                if existing_item.item == updated_item_data['item']:
                    foo = existing_item.quantity
                    bar = updated_item_data['quantity']
                    existing_item.quantity = updated_item_data['quantity']
                    existing_item.save()

                    #update original quantity count
                    foobar = updated_item_data['item']
                    foobar.quantity -= (bar-foo)
                    foobar.save()
                    
                    


        # Create new items for those not already associated with the Invoice

        item_data = [item_data for item_data in validated_data.get('items', [])]
        #print("item data := ", item_data)
        #new_items_data = [ item for item in item_data if item["item"] not in existing_items.values_list('item', flat=True)]
        existing_items_list = existing_items.values_list('item', flat=True)
        #print(existing_items_list)

        pq = [Item.objects.get(id=item) for item in existing_items_list]
        #print("pq := ", pq)
        new_items_data = []
        for item in item_data:
            if item["item"] not in pq:
                new_items_data.append(item)
            

        print("new items data := ", new_items_data)
        new_items = [BoughtItem.objects.create(**item_data) for item_data in new_items_data]

        print("new items", new_items)

        # Update quantities for associated items in the Item model
        for new_item_data in new_items_data:
            foo = new_item_data['item']
            foo.quantity -= new_item_data['quantity']
            foo.save()


        # Add existing and new bought items
        for items in new_items:
            instance.items.add(items)
        instance.save()

        return instance  

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
