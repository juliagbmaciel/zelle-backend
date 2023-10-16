from rest_framework import viewsets
from .serializers import ClientPhysicalSerializer
from .models import ClientPhysical


class ClientePhysicalViewSet(viewsets.ModelViewSet):
    queryset = ClientPhysical.objects.all()
    serializer_class = ClientPhysicalSerializer