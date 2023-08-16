from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        extra_field.setdefault('is_active', True)
        if extra_field.get('is_staff') is not True:
            raise ValueError('Superuser must be staff=True')
        if extra_field.get('is_superuser') is not True:
            raise ValueError('Superuser must be True')

        return self.create_user(email, password, **extra_field)
