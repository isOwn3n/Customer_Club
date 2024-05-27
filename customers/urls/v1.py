from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .. import views


router = DefaultRouter()
router.register("customer", views.CustomerViewSet, basename="customer")
router.register("group", views.GroupViewSet)
router.register(
    "restore_customer", views.CustomerRestoreViewSet, basename="restore-customer"
)
router.register("restore_group", views.GroupRestoreViewSet, basename="restore-group")
router.register("customer_count", views.CustomerCountViewSet, basename="customer-count")


urlpatterns = [
    path("", include(router.urls)),
]
