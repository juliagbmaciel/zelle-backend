from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model



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
    username = models.CharField(max_length=80, unique=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Address(models.Model):
    street = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"Cep {self.cep}"
    

class Client(models.Model):
    address_code = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    social_name = models.CharField(max_length=100, blank=True, null=True)
    picture = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField()

    class Meta:
        verbose_name = "Base Client"
        verbose_name_plural = "Base Clients"
    
    def __str__(self):
        return f"{self.name}"


class ClientPhysical(models.Model):
    client = models.OneToOneField('Client', on_delete=models.CASCADE, null=True)
    rg = models.CharField(max_length=18, blank=False)

    class Meta:
        verbose_name = "Physical Client"
        verbose_name_plural = "Physical Clients"

    def __str__(self):
        return str(self.client)


class ClientLegal(models.Model):
    client = models.OneToOneField('Client', on_delete=models.CASCADE)
    state_registration = models.CharField(max_length=200, blank=True)
    municipal_registration = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Legal Client"
        verbose_name_plural = "Legal Clients"
    
    def __str__(self):
        return self.client
    

class Account(models.Model):
    balance = models.FloatField(null=True, blank=True)
    agency = models.CharField(max_length=10)
    number = models.CharField(max_length=25, null=False)
    type = models.CharField(max_length=20, null=False)
    client = models.ManyToManyField('Client', null=True, blank=True)
    limit = models.DecimalField(max_digits=20, decimal_places=2)
    active = models.BooleanField()

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


    def __str__(self):
        return f"Conta {self.id}"


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=20,  null=True, blank=True)
    ramal = models.CharField(max_length=25,  null=True, blank=True)
    email = models.EmailField( null=True, blank=True)
    observation = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.number

class Investment(models.Model):
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
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    amount_requested = models.DecimalField(max_digits=20, decimal_places=2)
    cash_interest = models.FloatField()
    approved = models.BooleanField()
    number_installments = models.IntegerField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
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
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    number = models.CharField(max_length=30)
    cvv = models.CharField(max_length=5)
    expiration = models.DateField()
    banner = models.CharField(max_length=20)
    situation = models.CharField(max_length=20)
    limit = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
    
    def __str__(self):
        return self.number

class CardMovement(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    operation = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = "Card Movement"
        verbose_name_plural = "Card Movements"
    
    def __str__(self):
        return f"Valor de {self.value} no cartao com n° {self.card}"
    

class AccountMovement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(auto_now=True)
    operation = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = "Account Movement"
        verbose_name_plural = "Account Movements"
    
    def __str__(self):
        return f"Valor de {self.value} na conta com n° {self.account}"
