from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Store, Product, Sale, SaleDetail, Inventory


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('basic data'), {
            'fields': ('name',)
        }),
        (_('location'), {
            'fields': ('address', 'phone',)
        }),
    )
    list_display = ('name', 'address',)
    exclude = ('date_lst',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('basic data'), {
            'fields': ('name',)
        }),
        (_('commercial information'), {
            'fields': ('unit', 'price',)
        }),
    )
    list_display = ('name', 'unit', 'price',)
    search_fields = ('unit',)
    exclude = ('date_lst',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    fields = ('number', 'store',)
    search_fields = fields
    exclude = ('date_lst',)


@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('sale information'), {
            'fields': ('sale',)
        }),
        (_('detail'), {
            'fields': ('product', 'quantity', 'value',)
        }),
    )
    list_display = ('sale', 'product', 'quantity',)
    search_fields = ('product', 'sale',)
    exclude = ('date_lst',)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('location'), {
            'fields': ('store',)
        }),
        (_('inventory'), {
            'fields': ('product', 'available',)
        }),
    )
    list_display = ('store', 'product', 'available',)
    search_fields = ('store', 'product',)
    exclude = ('date_lst',)
