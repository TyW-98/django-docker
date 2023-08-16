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
    
    def create_superuser(self,email, password=None, **kwargs):
        return self.create_user(email,password, is_staff = True, is_superUser = True, **kwargs)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superUser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
 
    USERNAME_FIELD = "email"

