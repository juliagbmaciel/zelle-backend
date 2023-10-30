from rest_framework import serializers
from .models import User, ClientPhysical, Client, ClientLegal, Loan, Account, Card
import random
from django.utils import timezone

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


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    # client = ClientSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('agency', 'limit', 'active', 'number')

    def create(self, validated_data):
        default_balance = 0
        default_agency = random.choice(["0917-2", "0918-3", "0919-4", "0920-5", "0921-6"])
        default_limit = 1000000000000
        default_active = True

        account_type = validated_data.get('type', '')

        client_ids = validated_data.get('client', [])
        print(client_ids)
        if not client_ids:
            client = Client.objects.filter(user=self.context['request'].user.id).first()
            if client:
                
                client_ids = [client.id]

        account = Account.objects.create(
            balance=default_balance,
            agency=default_agency,
            limit=default_limit,
            active=default_active,
            type=account_type,
            number=create_number_account()
        )
        account.client.set(client_ids)

        return account


def create_number_account():
    while True:
        number_account = str(random.randint(1000000, 9999999))  
        if not Account.objects.filter(number=number_account).exists():
            return number_account



class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'

    def create(self, validated_data):
        account_id = self.context['request'].data.get('account')
        account = Account.objects.get(id=account_id)

        if account.balance < 500 or not account.active:
            raise serializers.ValidationError("Criação de cartão não autorizada", code="unauthorized")

        while True:
            generated_number = " ".join(["".join(random.choices("0123456789", k=4)) for _ in range(4)])
            if not Card.objects.filter(number=generated_number).exists():
                break

        cvv = "".join(random.choices("0123456789", k=3))
        banner = random.choice(["Visa", "Mastercard"])
        situation = "ativa"
        expiration = timezone.now() + timezone.timedelta(days=6 * 365)
        limit = 400.0

        card = Card(
            account=account,
            number=generated_number,
            cvv=cvv,
            banner=banner,
            situation=situation,
            expiration=expiration.date(),
            limit=limit
        )

        card.save()
        return card









        


      


