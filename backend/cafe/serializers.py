
from rest_framework import serializers

from .models import (
    ComputerType,
    Computer,
    Pricing,
    Service,
)


# 1. Компьютерийн төрөл
class ComputerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerType
        fields = '__all__'


# 2. Компьютерийн мэдээлэл
class ComputerSerializer(serializers.ModelSerializer):

    computer_type_name = serializers.CharField(
        source='computer_type.name',
        read_only=True
    )

    price_per_hour = serializers.SerializerMethodField()

    class Meta:
        model = Computer
        fields = [
            'id',
            'name',
            'computer_type',
            'computer_type_name',
            'status',
            'specifications',
            'price_per_hour',
        ]

    def get_price_per_hour(self, obj):
        pricing = Pricing.objects.filter(
            computer_type=obj.computer_type
        ).order_by('id').first()

        if pricing:
            return str(pricing.price_per_hour)

        return None


# 3. Үнийн тариф
class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'


# 4. Нэмэлт үйлчилгээ
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Customer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    phone = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'phone',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        Customer.objects.create(
            user=user,
            phone=phone
        )

        return user
