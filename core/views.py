from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import ClientPhysicalSerializer, ClientSerializer, ClientLegalSerializer, AccountSerializer, CardSerializer
from .models import ClientPhysical, Client, ClientLegal, Account, Card
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from django_filters import rest_framework as filters
import random


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()  
    serializer_class = ClientSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user:
            queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
    def partial_update(self, request, *args, **kwargs):
        user = request.user

        client = Client.objects.get(user=user)

        serializer = self.get_serializer(client, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



class ClientPhysicalViewSet(viewsets.ModelViewSet):
    queryset = ClientPhysical.objects.all()
    serializer_class = ClientPhysicalSerializer


    def get_queryset(self):
        user = self.request.user
        return ClientPhysical.objects.filter(client__user=user)

    def perform_create(self, serializer):
        client = Client.objects.filter(user=self.request.user).first()
        if client:
            serializer.save(client=client)
        
    def partial_update(self, request, *args, **kwargs):
        client_physical = ClientPhysical.objects.get(client__user=request.user)

        serializer = self.get_serializer(client_physical, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ClientLegalViewSet(viewsets.ModelViewSet):
    queryset = ClientLegal.objects.all()
    serializer_class = ClientLegalSerializer

    def get_queryset(self):
        user = self.request.user
        return ClientLegal.objects.filter(client__user=user)
            

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        existing_client_legal = ClientLegal.objects.filter(client__user=user).first()
        if existing_client_legal:

            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        client = Client.objects.filter(user=user).first()
        if client:
            serializer.save(client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Cliente não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        client_legal = ClientLegal.objects.get(client__user=request.user)

        serializer = self.get_serializer(client_legal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


# View que retorna o ID do cliente para facilitar uso da API (para atualizar clientes)
class GetClientIDView(APIView):
    def get(self, request):
        user = self.request.user
        try:
            client = Client.objects.get(user=user)
            client_id = client.id
            return Response({"client_id": client_id}, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({"detail": "Perfil de cliente não encontrado para este usuário."}, status=status.HTTP_404_NOT_FOUND)
        


def create_number_account():
    while True:
        number_account = str(random.randint(1000000, 9999999))  
        if not Account.objects.filter(number=number_account).exists():
            return number_account



class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        client = Client.objects.filter(user=self.request.user).first()
        if client:
            return client.account_set.all() 
        else:
            return Account.objects.none()

    
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()

    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     instance.save()

    #     return Response(self.get_serializer(instance).data)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



"""
Endpoint de criação de cartão, o método 
"""
class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('account',)
    search_fields = ('account')





