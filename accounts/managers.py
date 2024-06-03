from django.contrib.auth.models import UserManager
from django.contrib.auth import get_user_model


class CustomUserManager(UserManager):
    def create_staffuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)

        User = get_user_model()
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = User(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
