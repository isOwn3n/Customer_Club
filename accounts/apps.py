from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from django.contrib.auth import get_user_model
        from accounts.managers import CustomUserManager

        User = get_user_model()
        User.add_to_class("objects", CustomUserManager())
