from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import *


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if 0 >= value:
            raise serializers.ValidationError(_('price cannot be less than or equals zero'))


class InventorySerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    product = ProductSerializer()

    class Meta:
        model = Inventory
        fields = '__all__'

    def validate_available(self, value):
        if 0 > value:
            raise serializers.ValidationError(_('availability cannot be less than zero'))

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret


class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = '__all__'

    def to_internal_value(self, data):
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        # Perform the data validation.
        if not product_id:
            raise serializers.ValidationError({'product_id': _('This field is required')})
        if not quantity:
            raise serializers.ValidationError({'quantity': _('This field is required')})

        product = get_object_or_404(Product, id=product_id)

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'product': product_id,
            'quantity': quantity,
            'value': product.price * quantity
        }

    def create(self, validated_data):
        return SaleDetail(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

    def to_internal_value(self, data):
        number = data.get('number')
        details = data.get('details')

        # Perform the data validation.
        if not number:
            raise serializers.ValidationError({'number': _('This field is required')})
        if not details:
            raise serializers.ValidationError({'details': _('This list is required')})

        sale_details = []
        for detail in details:
            detail_serializer = SaleDetailSerializer(data=detail)
            detail_serializer.is_valid(raise_exception=True)
            sale_details.append(detail_serializer)

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'number': number,
            'details': details
        }

    def to_representation(self, obj):
        return {
            'number': obj.number,
            'player_name': obj.player_name
        }



