from rest_framework import serializers


class UserSearchesSerializer(serializers.Serializer):
    UUID = serializers.UUIDField()
    chat_id = serializers.IntegerField()
    pimbot_search_status = serializers.IntegerField()
    pimbot_results_adress = serializers.CharField()
    pimbot_delivery_status = serializers.BooleanField()
    findclone_search_status = serializers.IntegerField()
    findclone_preview = serializers.CharField()
    findclone_results_adress = serializers.CharField()
    findclone_results_count = serializers.IntegerField()
    def update(self, instance, validated_data):
        instance.UUID = validated_data.get('UUID', instance.UUID)
        instance.chat_id = validated_data.get('chat_id', instance.chat_id)
        instance.pimbot_search_status = validated_data.get('pimbot_search_status', instance.pimbot_search_status)
        instance.pimbot_results_adress = validated_data.get('pimbot_results_adress', instance.pimbot_results_adress)
        instance.pimbot_delivery_status = validated_data.get('pimbot_delivery_status', instance.pimbot_delivery_status)
        instance.findclone_search_status = validated_data.get('findclone_search_status', instance.findclone_search_status)
        instance.findclone_preview = validated_data.get('findclone_preview', instance.findclone_preview)
        instance.findclone_results_adress = validated_data.get('findclone_results_adress', instance.findclone_results_adress)
        instance.findclone_results_count = validated_data.get('findclone_results_count',
                                                               instance.findclone_results_count)
        instance.save()
        return instance

class UserSearchesSerializerPimeyes(serializers.Serializer):
    search_id = serializers.IntegerField()
    UUID = serializers.UUIDField()
    pimeyes_total_results_count = serializers.IntegerField()
    pimeyes_reletive_results_count = serializers.IntegerField()
    pimeyes_total_peec_count = serializers.IntegerField()
    pimeyes_search_status = serializers.IntegerField()
    pimeyes_results_delivered = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.id = validated_data.get('search_id', instance.id)
        instance.UUID = validated_data.get('UUID', instance.UUID)
        instance.pimeyes_total_results_count = validated_data.get('pimeyes_total_results_count', instance.pimeyes_total_results_count)
        instance.pimeyes_reletive_results_count = validated_data.get('pimeyes_reletive_results_count', instance.pimeyes_reletive_results_count)
        instance.pimeyes_total_peec_count = validated_data.get('pimeyes_total_peec_count', instance.pimeyes_total_peec_count)
        instance.pimeyes_search_status = validated_data.get('pimeyes_search_status', instance.pimeyes_search_status)
        instance.pimeyes_results_delivered = validated_data.get('pimeyes_results_delivered', instance.pimeyes_results_delivered)
        instance.save()
        return instance

