from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from django.utils import timezone


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, firstname, licence, password, **extra_fields):
        values = [email, name, firstname, licence]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            firstname=firstname,
            licence=licence,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, firstname, licence, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, firstname, licence, password, **extra_fields)

    def create_superuser(self, email, name, firstname, licence, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, firstname, licence, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, verbose_name="Nom")
    firstname = models.CharField(max_length=50, verbose_name="Prénom")
    licence = models.CharField(max_length=10, verbose_name="N° Licence")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'firstname', 'licence']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]
