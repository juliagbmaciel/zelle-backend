from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import ClientPhysicalSerializer, ClientSerializer, ClientLegalSerializer, AccountSerializer
from .models import ClientPhysical, Client, ClientLegal, Account
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
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

    def perform_create(self, serializer):
        client = Client.objects.filter(user=self.request.user).first()
        if client:
            serializer.save(client=client)

    def partial_update(self, request, *args, **kwargs):
        client_legal = ClientLegal.objects.get(client__user=request.user)

        serializer = self.get_serializer(client_legal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



# View que retorna o ID do cliente para facilitar uso da API
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
        number_account = str(random.randint(1000000, 9999999))  # Gere um número aleatório de 7 dígitos
        if not Account.objects.filter(number=number_account).exists():
            return number_account

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        client = Client.objects.filter(user=self.request.user).first()
        if client:
            return client.account_set.all()  # Acesse as contas relacionadas ao cliente
        else:
        # Trate o caso em que o cliente não foi encontrado
            return Account.objects.none()

    def create(self, request, *args, **kwargs):
        default_balance = 0
        default_agency = random.choice(["0917-2", "0918-3", "0919-4", "0920-5", "0921-6"])
        default_limit = 1000000000000
        default_active = True

        client_ids = request.data.get('client', [])
        account_type = request.data.get('type', '')


        account = Account(
            balance=default_balance,
            agency=default_agency,
            limit=default_limit,
            active=default_active,
            type=account_type,
            number = create_number_account()
        )
        account.save()
        account.client.set(client_ids) 

        serializer = self.get_serializer(account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        # Certifique-se de que limit, agency e number não sejam atualizados
        if 'limit' in request.data or 'agency' in request.data or 'number' in request.data:
            return Response(
                {"error": "Não é permitido atualizar limit, agency ou number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super(AccountViewSet, self).update(request, *args, **kwargs)

    
    def partial_update(self, request, *args, **kwargs):
        

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


