from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from datetime import datetime
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    image = models.ImageField(
        verbose_name=_("image"),
        upload_to="users",
        null=True,
        blank=True
    )

    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("description for any user"),
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def img_preview(self):
        try:
            return mark_safe(f'<img src="{self.image.url}" width = "50" height="40" alt="">')
        except Exception as e:
            return ""

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
