from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings


@api_view(["GET"])
def get_kavenegar_api(request):
    return Response(settings.KAVENEGAR_API_KEY, 200)
