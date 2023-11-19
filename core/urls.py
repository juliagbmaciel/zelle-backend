from rest_framework.routers import SimpleRouter
from .views import (ClientViewSet, 
                    ClientPhysicalViewSet, 
                    AccountViewSet, 
                    ClientLegalViewSet, 
                    CardViewSet,
                    LoanViewSet,
                    PayInstallmentView,
                    ClientDataView,
                    AddressViewSet,
                    ContactViewSet
                    )

from django.urls import path



router = SimpleRouter()
router.register('clients', ClientViewSet, basename='clients')
router.register('client-physical', ClientPhysicalViewSet, basename='client-physical')
router.register('client-legal', ClientLegalViewSet, basename='client-legal')
router.register('accounts', AccountViewSet, basename='account')
router.register('cards', CardViewSet, basename='card' )
router.register('loans', LoanViewSet, basename='loan')
router.register('address', AddressViewSet, basename='address')
router.register('contacts', ContactViewSet, basename='contacts')



urlpatterns = [
    path('pay-installments/<int:pk>', PayInstallmentView.as_view(), name='pay-loan'),
    path('view-installments', PayInstallmentView.as_view(), name='view-loan-installments'),
    path('client-all', ClientDataView.as_view(), name='client-data-all'),
]




