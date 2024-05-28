from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SendingMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=850)
    customers_id = serializers.ListField(child=serializers.IntegerField())
