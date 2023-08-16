from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    "Manager for custom user"

    def create_user(self, email, password=None, **kwargs):
        "Create and save new user."
        # email = email.split("@")[0] + "@" + email.split("@")[1].lower()
        if not email:
            raise ValueError("Email field is empty")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        """Create super user"""
        super_user = self.create_user(email, password, **kwargs)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using=self._db)

        return super_user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
