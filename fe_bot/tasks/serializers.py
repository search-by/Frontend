from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.Serializer):
    UUID = serializers.UUIDField()
    status = serializers.CharField()
    source_adres = serializers.CharField()
    chat_id = serializers.IntegerField()
    PY_max_results = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    class Meta:
        model = Task
        fields = ("source_adres", "chat_id", "status", "PY_max_results")
