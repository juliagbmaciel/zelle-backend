from rest_framework import serializers
from .models import User, ClientPhysical, Client, ClientLegal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            cpf=validated_data['cpf'],
            password=validated_data['password']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user



class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Client
        fields = "__all__"


class ClientPhysicalSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True) 
    class Meta:
        model = ClientPhysical
        fields = "__all__"


class ClientLegalSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True) 

    class Meta:
        model = ClientLegal
        fields = "__all__"