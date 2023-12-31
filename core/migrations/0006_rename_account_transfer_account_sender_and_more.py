# Generated by Django 4.2.6 on 2023-11-22 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_client_picture_alter_contact_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfer',
            old_name='account',
            new_name='account_sender',
        ),
        migrations.RenameField(
            model_name='transfer',
            old_name='card',
            new_name='card_sender',
        ),
        migrations.AddField(
            model_name='transfer',
            name='account_receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='core.account'),
        ),
        migrations.AlterField(
            model_name='account',
            name='client',
            field=models.ManyToManyField(to='core.client'),
        ),
    ]
