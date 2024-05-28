from django.urls import include, path
from messaging import views


urlpatterns = [
    path("send/", views.SendingMessageViewSet.as_view()),
    path("upload/<filename>", views.FileUploadView.as_view()),
]
