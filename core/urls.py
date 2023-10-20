from rest_framework.routers import SimpleRouter
from .viewsets import ClientViewSet, ClientPhysicalViewSet, GetClientIDView
from django.urls import path



router = SimpleRouter()
router.register('clients', ClientViewSet, basename='Client')
router.register('clients_physical', ClientPhysicalViewSet, basename='Client-Physical')
router.register('clients_legal', ClientViewSet, basename='Client-Legal')

urlpatterns = [
    path('clients/id', GetClientIDView.as_view(), name='Clients-Id'),
]

