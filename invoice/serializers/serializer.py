from rest_framework import serializers
from rest_framework.validators import ValidationError
from invoice.models  import *

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"