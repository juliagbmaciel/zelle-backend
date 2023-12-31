from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid



class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, password, **extra_fields):
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, cpf, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(cpf=cpf, password=password, **extra_fields)


class User(AbstractUser):
    cpf = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=80, unique=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"Cep {self.cep}"
    

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_code = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    social_name = models.CharField(max_length=100, blank=True, null=True)
    picture = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    birthdate = models.DateField()

    class Meta:
        verbose_name = "Base Client"
        verbose_name_plural = "Base Clients"
    
    def __str__(self):
        return f"{self.name}"


class ClientPhysical(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.OneToOneField('Client', on_delete=models.CASCADE, null=True)
    rg = models.CharField(max_length=18, blank=False)

    class Meta:
        verbose_name = "Physical Client"
        verbose_name_plural = "Physical Clients"

    def __str__(self):
        return str(self.client)


class ClientLegal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.OneToOneField('Client', on_delete=models.CASCADE)
    state_registration = models.CharField(max_length=200, blank=True)
    municipal_registration = models.CharField(max_length=200, blank=True)
    cnpj = models.CharField(max_length=40, null=True)

    class Meta:
        verbose_name = "Legal Client"
        verbose_name_plural = "Legal Clients"
    
    def __str__(self):
        return str(self.client)
    

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.FloatField(null=True, blank=True)
    agency = models.CharField(max_length=10)
    number = models.CharField(max_length=25, null=False)
    type = models.CharField(max_length=20, null=True)
    client = models.ManyToManyField('Client',  null=True)
    limit = models.DecimalField(max_digits=20, decimal_places=2)
    active = models.BooleanField()

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self): 
        clients_str = ", ".join(str(client) for client in self.client.all())
        return f"Clients: {clients_str}"


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=20, null=True)
    email = models.EmailField( null=True, blank=True)
    observation = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.number

class Investment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    contribution = models.DecimalField(max_digits=20, decimal_places=2)
    admin_tax = models.FloatField()
    deadline = models.CharField(max_length=20)
    risk_degree = models.CharField(max_length=5)
    profitability = models.DecimalField(max_digits=20, decimal_places=2)
    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Investment"
        verbose_name_plural = "Investments"

    def __str__(self):
        return f"Investimento da conta com {self.account}"

class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    request_date = models.DateField(auto_now_add=True)
    amount_requested = models.DecimalField(max_digits=20, decimal_places=2)
    cash_interest = models.FloatField(null=True)
    approved = models.BooleanField(null=True)
    number_installments = models.IntegerField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True, default=timezone.now().date())
    observation = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"
    
    def __str__(self):
        clients = ", ".join([client.name for client in self.account.client.all()])
        return f"Empréstimo da {self.account} do Cliente {clients}"


class LoanInstallment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    installment_number = models.IntegerField()
    due_date = models.DateField()
    installment_value = models.DecimalField(max_digits=20, decimal_places=2)
    pay_day = models.DateField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    

class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=30,null=True)
    cvv = models.CharField(max_length=5,null=True)
    expiration = models.DateField(null=True)
    banner = models.CharField(max_length=20, null=True)
    situation = models.CharField(max_length=20, null=True)
    limit = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True)
    limit_available = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True)

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
    
    def __str__(self):
        return str(self.id)

class CardMovement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    operation = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = "Card Movement"
        verbose_name_plural = "Card Movements"
    
    def __str__(self):
        return f"Valor de {self.value} no cartao com n° {self.card}"
    

# class CardBill(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     card = models.ForeignKey(Card, on_delete=models.CASCADE)
#     value_to_pay = models.CharField(max_length=300)
#     available_value = models.CharField(max_length=300)
#     due_date = models.DateField()
#     closing_date = models.DateField()

#     class Meta:
#         verbose_name = "Card Bill"
#         verbose_name_plural = "Card Bills"
    
#     def __str__(self):
#         return f"Fatura do cartão {self.card} do cliente {self.card__account__client}"
    

class AccountMovement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(auto_now=True)
    operation = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = "Account Movement"
        verbose_name_plural = "Account Movements"
    
    def __str__(self):
        return f"Valor de {self.value} na conta com n° {self.account}"


class Transfer(models.Model):
    TYPE_CHOICES = [
        ('conta', 'Conta'),
        ('cartao', 'Cartão de Crédito'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    account_sender = models.ForeignKey('Account', on_delete=models.CASCADE, blank=True, null=True)
    card_sender = models.ForeignKey('Card', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    account_receiver = models.ForeignKey('Account', on_delete=models.CASCADE, blank=True, null=True, related_name='receiver')

    def __str__(self):
        return f"Transferência - Tipo: {self.type}, Valor: {self.value}"