from rest_framework import viewsets
from .serializers import ClientPhysicalSerializer, ClientSerializer
from .models import ClientPhysical, Client
from rest_framework import filters



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()  
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # cpf = self.request.query_params.get('cpf')
        # print(cpf)
        print(self.request.user.id)
        if self.request.user:
            queryset = queryset.filter(user_id=self.request.user.id)
        return queryset


class ClientePhysicalViewSet(viewsets.ModelViewSet):
    queryset = ClientPhysical.objects.all()
    serializer_class = ClientPhysicalSerializer


