from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db import transaction

from .models import *

import logging
logger = logging.getLogger(__name__)


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
        depth = 1

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
        depth = 1

    def to_internal_value(self, data):
        product_id = data.get('product_id', None)
        if not product_id:
            return super().to_internal_value(data)

        quantity = data.get('quantity')
        if not quantity:
            raise serializers.ValidationError({'quantity': _('This field is required')})
        product = get_object_or_404(Product, id=product_id)

        value = data.get('value')
        if not value:
            value = product.price * quantity

        return {
            'product': product,
            'quantity': quantity,
            'value': value
        }


class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True, write_only=True)
    # store = StoreSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['number', 'store', 'details']
        depth = 1

    def to_internal_value(self, data):
        logger.info(f"data to_internal: {data}")
        details = data.get('details', None)
        store = data.get('store')
        if not store:
            raise serializers.ValidationError({'store': _('this field is required')})
        if not details:
            raise serializers.ValidationError({'details': _('this list is required')})
        if len(details) == 0:
            raise serializers.ValidationError({'details': _('this field is empty')})
        data = super().to_internal_value(data)
        data.update({'store': get_object_or_404(Store, id=store)})
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lst = []
        details = SaleDetail.objects.filter(sale_id=instance.id).values()
        for detail in details:
            lst.append(detail)

        data.update({'details': lst})
        return data

    @transaction.atomic
    def create(self, validated_data):
        details = validated_data.pop('details')
        sale = Sale.objects.create(**validated_data)
        for detail in details:
            try:
                inventory = Inventory.objects.get(store=validated_data['store'], product=detail['product'])
            except Inventory.DoesNotExist:
                sale.delete()
                logger.error(f"product {detail['product']} in store {validated_data['store']} not inventory")
                transaction.set_rollback(True)
                logger.error(f"Rollback transaction")
                raise serializers.ValidationError({'error', _('product not inventory in this store')})
            else:
                SaleDetail.objects.create(sale=sale, **detail)
                inventory.available -= 1
                logger.info(f"{detail['product']} {validated_data['store']} new balance {inventory.available}")
                inventory.save()
        return sale


