from rest_framework.permissions import DjangoModelPermissions
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Store, Product, Inventory, Sale, SaleDetail
from .serializers import StoreSerializer, ProductSerializer, InventorySerializer, SaleSerializer, SaleDetailSerializer

import logging
logger = logging.getLogger(__name__)


class StoreViewSet(ModelViewSet):
    """
    Store API
    ---
    retrieve:
        Return a store

    list:
        Return all stores

    create:
        Create a new store

    partial_update:
        Update one or more fields on an existing store

    update:
        Update a store
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProductViewSet(ModelViewSet):
    """
    Product API
    ---
    retrieve:
        Return a product

    list:
        Return all products

    create:
        Create a new product

    partial_update:
        Update one or more fields on an existing product

    update:
        Update a product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['^name']
    filterset_fields = ['price']

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class InventoryViewSet(ReadOnlyModelViewSet):
    """
    Inventory API
    ---
    retrieve:
        Return a inventory

    list:
        Return all inventories
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'product']


class SaleViewSet(ModelViewSet):
    """
    Sale API
    ---
    retrieve:
        Return a sale

    list:
        Return all sales

    create:
        Create a new sale

    partial_update:
        Update one or more fields on an existing sale

    update:
        Update a sale
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [DjangoModelPermissions]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['number', 'date']

    def create(self, request):
        """
        POST Example
        {
            "number": "1",
            "store": "1",
            "details": [
                {
                    "product_id": 1,
                    "quantity": 1
                },
                {
                    "product_id": 2,
                    "quantity": 3
                }
            ]
        }
        ---
         parameters:
        - number: body
          description: number of bull
          required: true
          paramType: body
        - store: body
          description: store id
          required: true
          paramType: body
        - details: details
          description: sale details
          required: true
          paramType: body
          pytype: SaleDetailSerializer
        ---
        """
        sale_serializer = SaleSerializer(data=request.data)
        sale_serializer.is_valid(raise_exception=True)
        # logger.info(f"serializer {serial}")
        sale = sale_serializer.create(sale_serializer.validated_data)
        return Response(sale, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SaleDetailViewSet(ReadOnlyModelViewSet):
    """
    Sale detail API
    ---
    retrieve:
        Return a sale detail

    list:
        Return all sale details
    """
    queryset = SaleDetail.objects.all()
    serializer_class = SaleDetailSerializer
    permission_classes = [DjangoModelPermissions]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['sale']
