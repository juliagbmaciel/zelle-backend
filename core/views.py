from rest_framework import viewsets
from .serializers import (ClientPhysicalSerializer, 
                          ClientSerializer, 
                          ClientLegalSerializer, 
                          AccountSerializer, 
                          CardSerializer,
                          LoanSerializer, 
                          LoanInstallmentSerializer,
                          )
from .models import (ClientPhysical, 
                     Client, 
                     ClientLegal, 
                     Account, 
                     Card, 
                     Loan, 
                     LoanInstallment,
                     )
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import generics, status
from django.utils import timezone


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()  
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClientPhysicalViewSet(viewsets.ModelViewSet):
    queryset = ClientPhysical.objects.all()
    serializer_class = ClientPhysicalSerializer

        
    def partial_update(self, request, *args, **kwargs):
        client_physical = ClientPhysical.objects.get(client__user=request.user)

        serializer = self.get_serializer(client_physical, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ClientLegalViewSet(viewsets.ModelViewSet):
    queryset = ClientLegal.objects.all()
    serializer_class = ClientLegalSerializer

            
    def partial_update(self, request, *args, **kwargs):
        client_legal = ClientLegal.objects.get(client__user=request.user)

        serializer = self.get_serializer(client_legal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('account',)
    search_fields = ('account')


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def perform_create(self, serializer):
        print("vamos de perform")
        serializer.save()

"""
View criada com o objetivo de APENAS atualizar e listar as parcelas de determinado emprestimo
"""
class PayInstallmentView(generics.UpdateAPIView, generics.ListAPIView):
    serializer_class = LoanInstallmentSerializer
    queryset = LoanInstallment.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        

        if instance.amount_paid is not None:
            return Response({"detail": "Esta parcela já foi paga."}, status=status.HTTP_400_BAD_REQUEST)
        
        amount_paid = request.data.get('amount_paid', None)
        
        if amount_paid is None:
            return Response({"detail": "O valor pago é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        if amount_paid < instance.installment_value:
            return Response({"detail": "O valor pago é inferior ao valor da parcela."}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.pay_day = timezone.now().date()
        instance.amount_paid = amount_paid
        instance.save()
        
        return Response({"detail": "Pagamento da parcela efetuado com sucesso."}, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        loan = self.request.data['loan']
        print(loan)
        if loan:
            return LoanInstallment.objects.filter(loan=loan).all()
        else:
            return LoanInstallment.objects.none()  
        
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
            





