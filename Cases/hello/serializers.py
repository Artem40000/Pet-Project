from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Items, ItemsTwo, ItemsThree



class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'pOne', 'pTwo', 'Url']

class ItemsTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsTwo
        fields = ['id', 'pOne', 'pTwo', 'Url']

class ItemsThreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsThree
        fields = ['id', 'pOne', 'pTwo', 'Url']