# Generated by Django 4.2.6 on 2023-10-18 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_card_movement'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Movement',
            new_name='CardMovement',
        ),
        migrations.AddField(
            model_name='card',
            name='limit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='AccountMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('operation', models.CharField(max_length=20)),
                ('value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.account')),
            ],
            options={
                'verbose_name': 'Account Movement',
                'verbose_name_plural': 'Account Movements',
            },
        ),
    ]
