from rest_framework import serializers


class MessageOutputSerializer(serializers.Serializer):
    message = serializers.CharField()
