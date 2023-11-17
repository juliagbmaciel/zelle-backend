from rest_framework import viewsets
from .serializers import (ClientPhysicalSerializer, 
                          ClientSerializer, 
                          ClientLegalSerializer, 
                          AccountSerializer, 
                          CardSerializer,
                          LoanSerializer, 
                          LoanInstallmentSerializer,
                          AddressSerializer,
                          ContactSerializer
                          )
from .models import (ClientPhysical, 
                     Client, 
                     ClientLegal, 
                     Account, 
                     Card, 
                     Loan, 
                     LoanInstallment,
                     Address,
                     Contact
                     )
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import generics, status
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404




class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print('queryset: ', queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        client = Client.objects.filter(user=self.request.user).first()
        if client:
            return [client]
        return []
    
    def get_mine_queryset(self):
        client = Client.objects.filter(user=self.request.user)
        print(client)
        if client:
            return [client]
        return []
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_mine_queryset())
        obj = get_object_or_404(queryset[0])
        self.check_object_permissions(self.request, obj)
        return obj

        
    
class ClientPhysicalViewSet(viewsets.ModelViewSet):
    serializer_class = ClientPhysicalSerializer

        
    def partial_update(self, request, *args, **kwargs):
        client_physical = ClientPhysical.objects.get(client__user=request.user)

        serializer = self.get_serializer(client_physical, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def get_queryset(self):
        client = Client.objects.filter(user=self.request.user).first()
        print(client)
        client_physical = ClientPhysical.objects.filter(client=client).first()
        if client_physical:
            return [client_physical]
        else: 
            raise ValidationError(detail='Este cliente não é físico.')


class ClientLegalViewSet(viewsets.ModelViewSet):
    queryset = ClientLegal.objects.all()
    serializer_class = ClientLegalSerializer

            
    def partial_update(self, request, *args, **kwargs):
        client_legal = ClientLegal.objects.get(client__user=request.user)

        serializer = self.get_serializer(client_legal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def get_queryset(self):
        client = Client.objects.filter(user=self.request.user).first()
        client_legal = ClientLegal.objects.filter(client=client).first()
        print(client_legal)
        if client_legal:
            return [client_legal]
        else: 
            raise ValidationError(detail='Este cliente não é jurídico.')

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_queryset(self):
        client = Client.objects.filter(user=self.request.user).first()
        if client:
            return Account.objects.filter(client=client)
        else:
            return Account.objects.none()

class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('account',)
    search_fields = ('account')


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


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
    


class ClientDataView(APIView):
    def get(self, request):
        user = request.user
        try:
            client = Client.objects.get(user=user)
            data = {"client": None, "account": None}

            if hasattr(client, 'clientphysical'):
                serializer = ClientPhysicalSerializer(client.clientphysical)
            elif hasattr(client, 'clientlegal'):
                serializer = ClientLegalSerializer(client.clientlegal)
            else:
                return Response({"detail": "Cliente não encontrado."}, status=404)

            data["client"] = serializer.data

            account = Account.objects.filter(client=client).first()
            if account:
                account_serializer = AccountSerializer(account)
                data["account"] = account_serializer.data

            return Response(data)
        except Client.DoesNotExist:
            return Response({"detail": "Cliente não encontrado."}, status=404)



class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    

    def get_queryset(self):
        user = self.request.user
        client = Client.objects.filter(user=user).first()

        # Retorna o QuerySet diretamente
        return Contact.objects.filter(client=client)
            





