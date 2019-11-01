from rest_framework import routers
from .views import InventoryViewSet, ProductViewSet, StoreViewSet, SaleViewSet, SaleDetailViewSet

router = routers.SimpleRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'store', StoreViewSet)
router.register(r'sale', SaleViewSet)
router.register(r'sale-detail', SaleDetailViewSet)

urlpatterns = router.urls
