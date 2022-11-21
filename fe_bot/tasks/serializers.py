from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.Serializer):
    UUID = serializers.UUIDField()
    status = serializers.CharField()
    source_adres = serializers.CharField()
    chat_id = serializers.IntegerField()
    PY_max_results = serializers.IntegerField()
    PY_tolerance = serializers.DecimalField(max_digits=5, decimal_places=3)
    FC_max_results = serializers.IntegerField()
    FC_tolerance = serializers.DecimalField(max_digits=5, decimal_places=3)
    send_full_results = serializers.BooleanField()
    send_fedback_request = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    class Meta:
        model = Task
        fields = ("source_adres", "chat_id", "status", "PY_max_results", "PY_tolerance",
                  "FC_max_results",
                  "FC_tolerance",
                  "send_full_results",
                  "send_fedback_request")
