from django.db import models
from django.utils.translation import ugettext_lazy as _


class Store(models.Model):
    name = models.CharField(
        _('name'),
        max_length=250,
        blank=False
    )
    address = models.CharField(
        _('address'),
        max_length=250,
        blank=True
    )
    phone = models.CharField(
        _('phone'),
        max_length=10,
        blank=True
    )
    date_lst = models.DateTimeField(
        _('last update date'),
        auto_now=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')
        db_table = "inventory_store"
        ordering = ['name']


class Product(models.Model):
    UNIT_UNITY = 'und'
    UNIT_PACKAGE = 'paq'
    UNIT_GRAM = 'gr'
    UNITS = (
        (UNIT_UNITY, _('unity')),
        (UNIT_PACKAGE, _('package')),
        (UNIT_GRAM, _('gram'))
    )
    name = models.CharField(
        _('name'),
        max_length=250,
        blank=False
    )
    unit = models.CharField(
        _('unit'),
        choices=UNITS,
        max_length=5
    )
    price = models.DecimalField(
        _('price'),
        max_digits=12,
        decimal_places=2,
        blank=False
    )
    date_lst = models.DateTimeField(
        _('last update date'),
        auto_now=True
    )

    def __str__(self):
        return f" {self.name} ({self.unit})"

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        db_table = "inventory_product"
        ordering = ['name']


class Inventory(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        verbose_name=_('store')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('store')
    )
    available = models.PositiveIntegerField(
        _('available'),
        default=0
    )
    date_lst = models.DateTimeField(
        _('last update date'),
        auto_now=True
    )

    def __str__(self):
        return f" {self.store} - {self.product} - {self.available}"

    class Meta:
        verbose_name = _('inventory')
        verbose_name_plural = _('inventory')
        db_table = "inventory_inventory"
        ordering = ['store', 'product']
        indexes = [
            models.Index(fields=['store']),
            models.Index(fields=['product']),
        ]


class Sale(models.Model):
    number = models.CharField(
        _('bill number'),
        max_length=250,
        blank=False
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.PROTECT,
        verbose_name=_('store')
    )
    date = models.DateField(
        _('bill date'),
        auto_now=True
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _('sale')
        verbose_name_plural = _('sales')
        db_table = "inventory_sale"
        ordering = ['-id']
        indexes = [
            models.Index(fields=['number']),
        ]


class SaleDetail(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        verbose_name=_('sale')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_('product')
    )
    quantity = models.PositiveSmallIntegerField(
        _('quantity'),
        blank=False
    )
    value = models.DecimalField(
        _('value'),
        max_digits=15,
        decimal_places=2,
        blank=False
    )
    date_lst = models.DateTimeField(
        _('last update date'),
        auto_now=True
    )

    def __str__(self):
        return f"{self.sale} - {self.product} - {self.quantity}"

    class Meta:
        verbose_name = _('sale detail')
        verbose_name_plural = _('sale details')
        db_table = "inventory_sale_detail"
        ordering = ['sale', 'product__name']
        indexes = [
            models.Index(fields=['sale']),
            models.Index(fields=['product']),
        ]
