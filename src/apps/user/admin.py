from django.contrib.admin import register, ModelAdmin, StackedInline
from . import models


class ProfileInline(StackedInline):
    model = models.Profile


@register(models.User)
class UserAdmin(ModelAdmin):
    list_display = ['phone', 'profile']

    inlines = [ProfileInline]
