from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager



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


# class Address(models.Model):
#     street = models.CharField(max_length=100)
#     neighborhood = models.CharField(max_length=75)
#     city = models.CharField(max_length=75)
#     state = models.CharField(max_length=2)
#     zip_code = models.CharField(max_length=10)

#     def __str__(self):
#         return f"Cep {self.cep}"
    

# class Client(models.Model):
#     address_code = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
#     name = models.CharField(max_length=100, null=False)
#     social_name = models.CharField(max_length=100, blank=True, null=True)
#     picture = models.CharField(max_length=100, blank=True, null=True)
#     birthdate = models.DateField()



# class ClientPhysical(models.Model):
#     client = models.OneToOneField('Client', on_delete=models.CASCADE)
#     user_cpf = models.ForeignKey(User, on_delete=models.CASCADE)
#     rg = models.CharField(max_length=18, blank=False)
    
    

# class Account(models.Model):
#     balance = models.FloatField(null=False)
#     agency = models.CharField(max_length=10, primary_key=True)
#     number = models.CharField(max_length=25, null=False)
#     type = models.CharField(max_length=20, null=False)
#     client = models.ManyToManyField('Client')
#     limit = models.DecimalField(max_digits=8, decimal_places=2)
#     ativa = models.BooleanField()

#     class Meta:
#         verbose_name = "Account"
#         verbose_name_plural = "Accounts"

#     def __str__(self):
#         return f"Agência {self.agency}"










