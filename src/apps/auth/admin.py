from django.contrib import admin
from .models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    fields = ('slug', 'name', 'permissions',)
    list_display = ('slug', 'name',)
    search_fields = ('slug', 'name',)
