from rest_framework import serializers


class PaginationInputSerializer(serializers.Serializer):
    page = serializers.IntegerField(min_value=1, default=1)


class MessageOutputSerializer(serializers.Serializer):
    message = serializers.CharField(default='ok')
