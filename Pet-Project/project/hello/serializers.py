from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(min_value=16, max_value=99)

    class Meta:
        model = Person
        fields = ['id', 'name', 'age', 'email', 'password']

    def validate(self, data):
        if data['age'] < 16 or data['age'] > 99:
            raise ValidationError("Возраст должен быть между 16 и 99")
        return data

    def create(self, validated_data):
        if 'name' not in validated_data or not validated_data['name'].strip():
            validated_data['name'] = "Неизвестно"
        return super().create(validated_data)