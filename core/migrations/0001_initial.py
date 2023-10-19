# Generated by Django 4.2.6 on 2023-10-19 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('cpf', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(max_length=80, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField()),
                ('agency', models.CharField(max_length=10)),
                ('number', models.CharField(max_length=25)),
                ('type', models.CharField(max_length=20)),
                ('limit', models.DecimalField(decimal_places=2, max_digits=20)),
                ('active', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100)),
                ('neighborhood', models.CharField(max_length=75)),
                ('city', models.CharField(max_length=75)),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30)),
                ('cvv', models.CharField(max_length=5)),
                ('expiration', models.DateField()),
                ('banner', models.CharField(max_length=20)),
                ('situation', models.CharField(max_length=20)),
                ('limit', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.account')),
            ],
            options={
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('social_name', models.CharField(blank=True, max_length=100, null=True)),
                ('picture', models.CharField(blank=True, max_length=100, null=True)),
                ('birthdate', models.DateField()),
                ('address_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.address')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Base Client',
                'verbose_name_plural': 'Base Clients',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now_add=True)),
                ('amount_requested', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cash_interest', models.FloatField()),
                ('approved', models.BooleanField()),
                ('number_installments', models.IntegerField(blank=True, null=True)),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('observation', models.CharField(blank=True, max_length=200, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.account')),
            ],
            options={
                'verbose_name': 'Loan',
                'verbose_name_plural': 'Loans',
            },
        ),
        migrations.CreateModel(
            name='LoanInstallment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_number', models.IntegerField()),
                ('due_date', models.DateField()),
                ('installment_value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('pay_day', models.DateField()),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
                ('contribution', models.DecimalField(decimal_places=2, max_digits=20)),
                ('admin_tax', models.FloatField()),
                ('deadline', models.CharField(max_length=20)),
                ('risk_degree', models.CharField(max_length=5)),
                ('profitability', models.DecimalField(decimal_places=2, max_digits=20)),
                ('finished', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.account')),
            ],
            options={
                'verbose_name': 'Investment',
                'verbose_name_plural': 'Investments',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=20, null=True)),
                ('ramal', models.CharField(blank=True, max_length=25, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('observation', models.CharField(blank=True, max_length=50, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.client')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='ClientPhysical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rg', models.CharField(max_length=18)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.client')),
            ],
            options={
                'verbose_name': 'Physical Client',
                'verbose_name_plural': 'Physical Clients',
            },
        ),
        migrations.CreateModel(
            name='ClientLegal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_registration', models.CharField(blank=True, max_length=200)),
                ('municipal_registration', models.CharField(blank=True, max_length=200)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.client')),
            ],
            options={
                'verbose_name': 'Legal Client',
                'verbose_name_plural': 'Legal Clients',
            },
        ),
        migrations.CreateModel(
            name='CardMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('operation', models.CharField(max_length=20)),
                ('value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.card')),
            ],
            options={
                'verbose_name': 'Card Movement',
                'verbose_name_plural': 'Card Movements',
            },
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
        migrations.AddField(
            model_name='account',
            name='client',
            field=models.ManyToManyField(to='core.client'),
        ),
    ]
