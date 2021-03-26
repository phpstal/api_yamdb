from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES_CHOICES = [
    ('user', 'Пользователь'),
    ('moderator','Модератор'),
    ('admin', 'Администратор'),
]

class YamdbUser(AbstractUser):
    email = models.EmailField(verbose_name='E-Mail', unique=True)
    bio = models.TextField(verbose_name='О себе', blank=True)
    code = models.TextField(verbose_name='Код', blank=True)
    username = models.CharField(
        max_length=70,
        verbose_name='Имя пользователя',
        blank=True
    )
    role = models.CharField(
        default='user',
        max_length=10,
        verbose_name='Роль',
        choices=ROLES_CHOICES
    )
    user_permissions = None
    groups = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
