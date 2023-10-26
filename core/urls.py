from rest_framework.routers import SimpleRouter
from .viewsets import ClientViewSet, ClientPhysicalViewSet, GetClientIDView, AccountViewSet
from django.urls import path



router = SimpleRouter()
router.register('clients', ClientViewSet, basename='Client')
router.register('client-physical', ClientPhysicalViewSet, basename='Client-Physical')
router.register('client-legal', ClientViewSet, basename='Client-Legal')
router.register('account', AccountViewSet, basename='Account')

urlpatterns = [
    path('clients/id', GetClientIDView.as_view(), name='Clients-Id'),
]

