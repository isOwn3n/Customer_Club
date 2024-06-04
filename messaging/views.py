import re

from rest_framework import views, parsers, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from messaging.utils import convert_file
from messaging.utils.send.sending import check_sending_message_is_possible
from messaging.tasks import send

from . import serializers


class FileUploadView(views.APIView):
    """This is an endpoint to upload file to import bulk customers from telegram."""

    parser_classes = [parsers.FileUploadParser, parsers.MultiPartParser]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, filename, format=None):
        """File form names would be like this two, file and name_include as boolean"""

        file_obj = request.FILES["file"]

        is_name_included = request.data.get("name_include", True)
        if isinstance(is_name_included, str):
            is_name_included = True if str(convert_file).lower() == "true" else False

        decoded_file_data = file_obj.read().decode()
        json_data = re.search(
            r"(?<=application/json\n\n)(.*?)(?=\n--)", decoded_file_data, re.DOTALL
        ).group(  # type: ignore
            1
        )
        result = convert_file.customers_from_telegram(json_data, is_name_included)
        return Response(result, status=status.HTTP_201_CREATED)


class SendingMessageViewSet(viewsets.ViewSet):
    serializer_class = serializers.SendingMessageSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            message = validated_data.get("message", "")  # type: ignore
            customers_id = validated_data.get("customers_id", "")  # type: ignore
            check_possibility = check_sending_message_is_possible(message, len(customers_id))
            if isinstance(check_possibility, tuple):
                send.send_message.delay(message, customers_id)
                return Response({"cost": check_possibility[1]}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ActionViewSet
