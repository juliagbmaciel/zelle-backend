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
    LoanInstallment
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












# @admin.register(Carro)
# class CarroAdmin(admin.ModelAdmin):
#     list_display = ('montadora', 'modelo', 'chassi', 'preco', 'get_motoristas')

#     def get_motoristas(self, obj):
#         return ', '.join([m.username for m in obj.motoristas.all()])

#     get_motoristas.short_description = 'Motoristas'