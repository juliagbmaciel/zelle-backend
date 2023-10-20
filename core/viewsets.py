from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import ClientPhysicalSerializer, ClientSerializer, ClientLegalSerializer
from .models import ClientPhysical, Client, ClientLegal
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response



#View que cria, atualiza e lê o model cliente
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()  
    serializer_class = ClientSerializer
    
    # Pega o cliente de acordo com o token
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user:
            queryset = queryset.filter(user_id=self.request.user.id)
        return queryset
    
    # Cria o campo usuario de acordo com o token 
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Atualiza de acordo com os campos enviados, não precisa enviar o objeto todo
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

    # filtra o cliente de acordo com o token
    def get_queryset(self):
        user = self.request.user
        return ClientPhysical.objects.filter(client__user=user)

    # salva o campo cliente de acordo com o token
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

    # filtra o cliente de acordo com o token
    def get_queryset(self):
        user = self.request.user
        return ClientLegal.objects.filter(client__user=user)

    # salva o campo cliente de acordo com o token
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