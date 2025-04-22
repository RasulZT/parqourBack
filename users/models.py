from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from utils.enums import LanguageCode


class CustomUserManager(BaseUserManager):
    def create_user(self, telegram_id, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("Пользователь должен иметь telegram_id")
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(telegram_id, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.CharField(max_length=255, unique=True)
    telegram_fullname = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=128, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(max_length=2, choices=LanguageCode.choices, default=LanguageCode.RU)
    parkings = models.ManyToManyField('services.Parking', related_name='users', blank=True)
    operators = models.ManyToManyField('self', symmetrical=False, related_name='assigned_by', blank=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('support', 'Support'),
        ('client', 'Client')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.telegram_fullname or str(self.telegram_id)
