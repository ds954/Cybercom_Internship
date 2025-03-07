from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email), name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, name, password=None, **extra_fields):
        user= self.create_user(email, name=name, password=password, **extra_fields)
        user.is_admin=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email=models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True
    )
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name"]

    objects=UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


