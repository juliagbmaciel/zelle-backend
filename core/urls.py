from rest_framework.routers import SimpleRouter
from .viewsets import ClientViewSet



router = SimpleRouter()
router.register('clients', ClientViewSet, basename='Client')

