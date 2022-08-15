from rest_framework import serializers
from .models import Task

class TaskStatusSerializer(serializers.Serializer):
    UUID = serializers.UUIDField()
    status = serializers.CharField()
    pimeyes_status = serializers.IntegerField()

    def update(self, instance, validated_data):
        status_old = int(instance.pimeyes_status)
        status_new = int(validated_data['pimeyes_status'])
        if status_new > status_old or status_new == 0:
            instance.status = validated_data.get("status", instance.status)
            instance.pimeyes_status = validated_data.get("pimeyes_status", instance.pimeyes_status)
            instance.save()
        else:
            return False
        return instance

    def change_status(self, instance, validated_data):
        status_old = instance.status
        status_new = validated_data['pimeyes_status']
        if status_new > status_old or status_new == 1:
            instance.save()
        else:
            return False


    class Meta:
        model = Task
        fields = ("UUID", "status", "pimeyes_status")

