from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime

ADMIN = "ADMIN"
EMPLOYEE = "EMPLOYEE"
MANAGER = "MANAGER"

ROLES = (
    (ADMIN, "Admin"),
    (EMPLOYEE, "Employee"),
    (MANAGER, "Manager")
)


class MainUserManager(BaseUserManager):
    def create_user(self, email, password, fio=None, camunda_id=None, phone=None, image_url=None, image_url_orig=None):
        if not email:
            raise ValueError('User must have a email')
        email = self.normalize_email(email)
        user = self.model(email=email, fio=fio, camunda_id=camunda_id, phone=phone, image_url=image_url,
                          image_url_orig=image_url_orig)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class MainUser(AbstractBaseUser, PermissionsMixin):
    camunda_id = models.CharField(max_length=160, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True, verbose_name='email сотрудника')
    fio = models.CharField(max_length=100, verbose_name='ФИО сотрудника', null=True, blank=True)
    is_active = models.IntegerField(default=1,
                                    verbose_name='Признак активности. 0 - не активный, 1 - активный. По умолчанию 1')
    last_login = models.DateTimeField(editable=True, blank=True, null=True,
                                      verbose_name='Дата и время последнего входа в систему')
    rowversion = models.DateField(editable=True, blank=True, null=True, verbose_name='Дата и время изменения')
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Телефон сотрудника')
    image_url = models.TextField(blank=True, null=True, verbose_name='Аватарка')
    image_url_orig = models.TextField(blank=True, null=True, verbose_name='Аватар оригинал')
    is_show_all_remonts = models.IntegerField(default=0, verbose_name='Показывать вес ремонты для данной должности')
    is_write_chat_message = models.IntegerField(default=0, verbose_name='Может ли писать в чат (1 - да, 0 - нет')
    mobile_token_id = models.CharField(max_length=20, blank=True, null=True,
                                       verbose_name='Первые 10 символов от mobile')
    is_kpi = models.IntegerField(default=0, verbose_name='Возможность проставлять KPI')
    is_only_read = models.IntegerField(default=0,
                                       verbose_name='1 - пользователь только для чтения, 0 - обычный наш пользователь')
    is_subscribe = models.IntegerField(default=0,
                                       verbose_name='Подписан ли пользователь на уведомления. 0 - не подписан, 1 - подписан')
    application_code = models.CharField(max_length=50, blank=True, null=True,
                                        verbose_name='На какое приложение отправлять пуш уведомление')
    guid = models.CharField(max_length=250, blank=True, null=True, verbose_name='ГУИД для хантеров в 1С')
    is_staff = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=500, blank=True, null=True)
    USERNAME_FIELD = 'email'
    objects = MainUserManager()
