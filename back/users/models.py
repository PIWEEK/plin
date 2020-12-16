from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },
        blank=True, null=True
    )
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
