from django.urls import include, path
from messaging import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("send", views.SendingMessageViewSet, "send")


urlpatterns = [
    path("", include(router.urls)),
    path("upload/<filename>", views.FileUploadView.as_view()),
]
