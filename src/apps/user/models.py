from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser):
    USERNAME_FIELD = 'phone'
    objects = UserManager()

    phone = models.CharField(verbose_name='Phone', max_length=11, unique=True, blank=False, null=False)

    is_admin = models.BooleanField(verbose_name='Is Admin', default=False)
    is_active = models.BooleanField(verbose_name='Is Active', default=True)

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            profile = self.profile
        except Profile.DoesNotExist:
            profile = Profile(user_id=self.id)
            profile.save()

    def get_full_name(self):
        return f'{self.profile.first_name} {self.profile.last_name}'

    def get_short_name(self):
        return self.profile.first_name

    def get_user_permissions(self, obj=None):
        return []

    def get_group_permissions(self, obj=None):
        return []

    def get_all_permissions(self, obj=None):
        return []

    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True

        return False

    def has_perms(self, perm_list, obj=None):
        if self.is_admin:
            return True

        return False

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True

        return False


class Profile(models.Model):
    user = models.OneToOneField(verbose_name='User', to=User, on_delete=models.CASCADE, related_name='profile',
                                blank=False, null=False)

    first_name = models.CharField(verbose_name='Firstname', max_length=30)
    last_name = models.CharField(verbose_name='Lastname', max_length=30)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
