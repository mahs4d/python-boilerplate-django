from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, is_admin=False, is_active=True, **extra_fields):
        if not phone:
            raise ValueError('phone should be provided')

        user = self.model(phone=phone, is_admin=is_admin, is_active=is_active, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        return self.create_user(phone=phone, password=password, is_admin=True, is_active=True, **extra_fields)
