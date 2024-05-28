# import pytest
# from django.conf import settings


# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass


# @pytest.fixture(scope="session")
# def django_db_setup():
#     settings.DATABASES["default"] = {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": ":memory:",
#     }


# @pytest.fixture(scope="session")
# def django_db_modify_db_settings():
#     settings.DATABASES["default"]["ATOMIC_REQUESTS"] = True


# @pytest.fixture(autouse=True)
# def enable_rest_framework_settings():
#     settings.REST_FRAMEWORK = {
#         # Add your REST framework settings here
#         "DEFAULT_AUTHENTICATION_CLASSES": (
#             "rest_framework_simplejwt.authentication.JWTAuthentication",
#         ),
#         # "DEFAULT_PERMISSION_CLASSES": [
#         #     "rest_framework.permissions.IsAuthenticated",
#         # ],
#     }
