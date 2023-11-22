# Generated by Django 4.2.6 on 2023-11-22 12:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_merge_20231117_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='approval_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 11, 22), null=True),
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('conta', 'Conta'), ('cartao', 'Cartão de Crédito')], max_length=10)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.account')),
                ('card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.card')),
            ],
        ),
    ]