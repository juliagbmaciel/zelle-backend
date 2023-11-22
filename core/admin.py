from django.contrib import admin
from .models import (
    User, 
    Account, 
    Address, 
    Client, 
    ClientLegal, 
    ClientPhysical, 
    Investment,
    Loan,
    LoanInstallment,
    Contact,
    Card,
    CardMovement,
    AccountMovement,
    Transfer
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'username')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('balance', 'agency', 'number', 'type', 'limit', 'active', 'list_clients')

    def list_clients(self, obj):
        return ", ".join([client.name for client in obj.client.all()])
    list_clients.short_description = "Clients"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'social_name', 'picture', 'birthdate')


@admin.register(ClientPhysical)
class ClientPhysicalAdmin(admin.ModelAdmin):
    list_display = ('client', 'user_cpf', 'rg')

    def user_cpf(self, obj):
        return obj.client.user


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('account', 'type', 'contribution')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('account', 'request_date', 'amount_requested', 'approved', 'cash_interest')



@admin.register(LoanInstallment)
class LoanInstallmentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'installment_number', 'due_date', 'installment_value', 'pay_day')


@admin.register(ClientLegal)
class ClientLegalAdmin(admin.ModelAdmin):
    list_display =('client', 'state_registration', 'municipal_registration')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('client', 'number', 'email', 'observation')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'neighborhood', 'city', 'state', 'zip_code')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('account', 'number', 'cvv', 'expiration', 'banner', 'situation', 'limit', 'limit_available')

@admin.register(CardMovement)
class CardMovementAdmin(admin.ModelAdmin):
    list_display = ('card', 'date_time', 'operation', 'value')


@admin.register(AccountMovement)
class AccountMovementAdmin(admin.ModelAdmin):
    list_display = ('account', 'date_time', 'operation', 'value')



@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('type', 'value', 'account_sender', 'card_sender', 'date', 'account_receiver')


