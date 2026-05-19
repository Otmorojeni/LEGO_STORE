from django.db import models

from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Theme(models.Model):
    """Модель тематики"""

    name = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.name
    

class Brand(models.Model):
    """Модель бренда"""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
    

class Kit(models.Model):
    """Модель набора"""

    article = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    theme = models.ForeignKey(
        Theme, 
        on_delete=models.CASCADE,
        related_name='kits'
    )
    details_count = models.PositiveIntegerField()
    release_year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.article} {self.name}'
    

class Review(models.Model):
    """Модель отзыва"""

    kit = models.ForeignKey(
        Kit,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer_name = models.CharField(max_length=150)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='comments'
    )

    def __str__(self) -> str:
        return f'Отзыв для {self.kit.name} от {self.reviewer_name}'
    

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email