from rest_framework import serializers
from .models import (User, 
                     ClientPhysical, 
                     Client, 
                     ClientLegal, 
                     Loan, 
                     Account, 
                     Card, 
                     LoanInstallment,
                     Address,
                     Contact)
import random
from django.utils import timezone
from django.db.models.signals import post_save
from .signals import loan_installment_signal 
from rest_framework.exceptions import ValidationError


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

    def create(self, validated_data):
        user = self.context['request'].user
        client_data = validated_data

        if Client.objects.filter(user=user).first():
            raise ValidationError("Este usuário já possui um cliente associado.", code='invalid')
        
        client = Client.objects.create(
            name=client_data['name'],
            social_name=client_data.get('social_name', None),
            picture=client_data.get('picture', None),
            birthdate=client_data['birthdate'],
            user=user  
        )
        
        if 'address_code' in client_data:
            client.address_code = client_data['address_code']
        
        client.save()
        
        return client
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.social_name = validated_data.get('social_name', instance.social_name)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)

        if 'address_code' in validated_data:
            instance.address_code = validated_data['address_code']

        instance.save()
        
        return instance



class ClientPhysicalSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True) 
    class Meta:
        model = ClientPhysical
        fields = "__all__"

    def create(self, validated_data):
        client = Client.objects.filter(user=self.context['request'].user).first()

        if ClientPhysical.objects.filter(client=client).first() or ClientLegal.objects.filter(client=client).first():
            raise serializers.ValidationError("Este usuário já possui um cliente físico ou legal associado.")
        
        client_data = validated_data
        if client:
            client_physical = ClientPhysical.objects.create(
                rg=client_data['rg'],
                client=client
            )

            return client_physical
        else:
            raise serializers.ValidationError("Algo deu errado na criação do cliente.")



class ClientLegalSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False, read_only=True) 

    class Meta:
        model = ClientLegal
        fields = "__all__"

    def create(self, validated_data):
        client = Client.objects.filter(user=self.context['request'].user).first()

        if ClientPhysical.objects.filter(client=client).first() or ClientLegal.objects.filter(client=client).first():
            raise serializers.ValidationError("Este usuário já possui um cliente físico ou legal associado.")
        
        client_data = validated_data
        if client:
            client_legal = ClientLegal.objects.create(
                cnpj=client_data['cnpj'],
                state_registration=client_data['state_registration'],
                municipal_registration=client_data['municipal_registration'],
                client=client
            )
            return client_legal
        else:
            raise serializers.ValidationError("Algo deu errado na criação do cliente.")


    

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

        if not client_ids:
            client = Client.objects.filter(user=self.context['request'].user.id).first()

            if Account.objects.filter(client=client).first():
                print(Account.objects.filter(client=client).first())
                raise serializers.ValidationError("Este cliente ja possui uma conta.")
            
            if client:
                client_ids = [client.id]
            else:
                raise serializers.ValidationError("Este usuário não está atrelado a nenhum cliente.")

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



class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        address = Address(
            street = validated_data['street'],
            neighborhood = validated_data['neighborhood'],
            city = validated_data['city'],
            state = validated_data['state'],
            zip_code = validated_data['zip_code']
        )
        address.save()
        return address

"""

            street = validated_data['street'],
            neighborhood = validated_data['neighborhood'],
            city = validated_data['city'],
            state = validated_data['state'],
            zip_code = validated_data['zip_code']
class Address(models.Model):
    street = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"Cep {self.cep}"

"""

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'

    def create(self, validated_data):
        client = Client.objects.filter(user=self.context['request'].user).first()
        account = Account.objects.get(client=client)
        print(account)
        

        if not account.active:
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

class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = '__all__'
    
    def create(self, validated_data):
        client = Client.objects.filter(user=self.context['request'].user).first()
        account = Account.objects.get(client=client)
        amount_requested = validated_data['amount_requested']
        cash_interest = 9

        if account.balance < 1000:
            post_save.disconnect(loan_installment_signal, sender=Loan)
            loan = Loan.objects.create(
                account = account,
                amount_requested = amount_requested,
                cash_interest = cash_interest,
                approved = False,
                number_installments = validated_data['number_installments'],
                approval_date = None,
                observation = "Não fora autorizada a solicitação de emprestimo"
            )
            post_save.connect(loan_installment_signal, sender=Loan)
            loan.save()

            raise serializers.ValidationError("Conta não atende os requisitos para realização de emprestimo", code="unauthorized")
        
        else:
       
            post_save.disconnect(loan_installment_signal, sender=Loan)
            loan = Loan.objects.create(
                account = account,
                amount_requested = amount_requested,
                cash_interest = cash_interest,
                approved = True,
                number_installments = validated_data['number_installments'],
                observation = "Empréstimo autorizado."
            )
            post_save.connect(loan_installment_signal, sender=Loan)
            loan.save()
            
            return loan
    
    def get_queryset(self):
        client = Client.objects.filter(user=self.context['request'].user).first()
        account = Account.objects.filter(account=account).first()
        if account:
            return Loan.objects.filter(account=account)
        else:
            return Loan.objects.none()


class LoanInstallmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanInstallment
        fields = '__all__'



class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'

    def create(self, validated_data):
        client = Client.objects.filter(user=self.context['request'].user).first()


        validated_data['client'] = client

        model_fields = [field.name for field in Contact._meta.get_fields()]
        filtered_data = {key: value for key, value in validated_data.items() if key in model_fields}

        instance = Contact.objects.create(**filtered_data)

        return instance






        


      


