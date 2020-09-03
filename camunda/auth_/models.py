
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)
from django.db import models

ADMIN = "ADMIN"
EMPLOYEE = "EMPLOYEE"
MANAGER = "MANAGER"

ROLES = (
    (ADMIN, "Admin"),
    (EMPLOYEE, "Employee"),
    (MANAGER, "Manager")
)


class MainUserManager(BaseUserManager):
    def create_user(self, username, password,first_name=None, last_name=None):
        if not username:
            raise ValueError('User must have a username')
        email = username + "@camunda.org"
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name,
                          last_name=last_name, full_name=first_name+" "+last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.is_admin = True
        user.is_manager = True
        user.is_staff = True
        user.role = ADMIN
        user.save(using=self._db)
        return user


class MainUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    full_name = models.CharField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    role = models.CharField(max_length=100, choices=ROLES, default=EMPLOYEE, verbose_name="Роль")
    timestamp = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    objects = MainUserManager()

