# Generated by Django 4.2.6 on 2023-11-08 14:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientlegal',
            name='cnpj',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='client',
            field=models.ManyToManyField(null=True, to='core.client'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.account'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='approval_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 11, 8), null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='approved',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='cash_interest',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=80),
        ),
    ]
