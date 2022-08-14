from rest_framework import serializers
from .models import BotSettings

class BotSettindsSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.CharField()
    free_mounth = serializers.IntegerField()
    free_day = serializers.IntegerField()
    additional_search_price = serializers.DecimalField()
    pimeyes_results_count = serializers.IntegerField()
    findclone_results_count = serializers.IntegerField()

    class Meta:
        model = BotSettings
        fields = '__all__'