from rest_framework.routers import SimpleRouter
from .views import ClientViewSet, ClientPhysicalViewSet, GetClientIDView, AccountViewSet, ClientLegalViewSet, CardViewSet
from django.urls import path



router = SimpleRouter()
router.register('clients', ClientViewSet, basename='Client')
router.register('client-physical', ClientPhysicalViewSet, basename='Client-Physical')
router.register('client-legal', ClientLegalViewSet, basename='Client-Legal')
router.register('account', AccountViewSet, basename='Account')
router.register('cards', CardViewSet, basename='Cards' )

urlpatterns = [
    path('clients/id', GetClientIDView.as_view(), name='Clients-Id'),
    # path('create-card/', CreateCardView.as_view(), name='Create Card'),
]

