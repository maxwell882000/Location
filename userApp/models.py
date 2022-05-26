from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """
    Django требует, чтобы пользовательские `User`
    определяли свой собственный класс Manager.
    Унаследовав от BaseUserManager, мы получаем много кода,
    используемого Django для создания `User`.

    Все, что нам нужно сделать, это переопределить функцию
    `create_user`, которую мы будем использовать
    для создания объектов `User`.
    """

    def _create_user(self, phone, password=None, **extra_fields):

        if not phone:
            raise ValueError('Данный адрес электронной почты должен быть установлен')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """
        Создает и возвращает пользователя с правами
        суперпользователя (администратора).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(db_index=True, max_length=50)
    lastname = models.CharField(db_index=True, max_length=50)
    phone = models.CharField(db_index=True, unique=True, max_length=50)
    is_staff = models.BooleanField(default=False)
    is_phone_reset_validate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_phone_validated = models.BooleanField(default=False)
    is_email_validated = models.BooleanField(default=False)
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ('firstname', 'lastname')
    object = UserManager()

    @property
    def fullname(self):
        return "{} {}".format(self.firstname, self.lastname)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name_plural = "Пользователи"

    @property
    def token(self):
        return self._generate_token()[0].key

    def get_short_name(self):
        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Как правило, это будет имя пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """
        return self.fullname

    def _generate_token(self):
        return Token.objects.get_or_create(user=self)


class CodeOTP(models.Model):
    code = models.IntegerField()
    user = models.OneToOneField('User', on_delete=models.CASCADE)
