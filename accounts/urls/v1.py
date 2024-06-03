from django.urls import include, path
from accounts import views

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

router = DefaultRouter()
router.register("me", views.MeViewSet, "me")
router.register("user", views.UserViewSet)
router.register("change-password", views.ChangePasswordViewSet, "change-password")
router.register(
    "admin-change-password", views.ChangePasswordByAdminViewSet, "admin-change-password"
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
]
