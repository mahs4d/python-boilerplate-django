from django.conf import settings
from django.contrib.postgres import fields as postgres_fields
from django.db import models


class Role(models.Model):
    slug = models.SlugField(verbose_name='slug', unique=True, blank=False)
    name = models.CharField(verbose_name='name', max_length=50, blank=False)
    users = models.ManyToManyField(to='pb_user.User', related_name='roles')
    permissions = postgres_fields.ArrayField(verbose_name='permissions list (slugs)',
                                             base_field=models.CharField(max_length=50),
                                             default=list, blank=True)

    def save(self, *args, **kwargs):
        if self.slug == 'admin':
            raise ValueError('role cannot have "admin" slug')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OtpCode(models.Model):
    user = models.ForeignKey(to='pb_user.User', on_delete=models.CASCADE,
                             related_name='otp_codes', related_query_name='otp_code',
                             db_index=True, blank=False)
    code = models.CharField(verbose_name='otp code', max_length=settings.OTP_CODE_LENGTH, blank=False)
    is_used = models.BooleanField(verbose_name='is used', db_index=True, default=False)
    creation_time = models.DateTimeField(verbose_name='creation time', auto_now=True, db_index=True, blank=False)

    class Meta:
        ordering = ('-creation_time',)
