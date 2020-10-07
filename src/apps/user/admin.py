from django.apps import apps
from django.contrib.admin import ModelAdmin, register, StackedInline

from . import models


class ProfileInline(StackedInline):
    model = models.Profile


class RoleInline(StackedInline):
    model = apps.get_model('pb_auth', 'Role').users.through
    extra = 0


@register(models.User)
class UserAdmin(ModelAdmin):
    list_display = ['phone', 'profile']

    inlines = [ProfileInline, RoleInline]
