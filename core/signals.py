from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan, LoanInstallment
from datetime import timedelta
from decimal import Decimal


@receiver(post_save, sender=Loan)
def testando_signal(sender, instance, **kwargs):
    if instance.approved and instance.number_installments:
        cash_interest = instance.cash_interest
        juro = (cash_interest / 100) * float(instance.amount_requested)
        valor_total = instance.amount_requested + Decimal(juro)
        valor_parcela = valor_total / instance.number_installments
        due_date = instance.approval_date + timedelta(days=30)
        for i in range(1, instance.number_installments + 1):
            LoanInstallment.objects.create(
                loan=instance,
                installment_number=i,
                due_date=due_date,
                installment_value=valor_parcela,
                pay_day=None,
                amount_paid=None
            )
            due_date += timedelta(days=30)