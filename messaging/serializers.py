from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SendingMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=850)
    customers_id = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
    )
    groups_id = serializers.ListField(child=serializers.IntegerField(), required=False)


# TODO: Complete this serializer to user be able to schedule message send time.
class ScheduleTaskSerializer(serializers.Serializer):
    run_at = serializers.DateTimeField()
    # data = serializers.
